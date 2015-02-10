from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic import TemplateView, DetailView, DeleteView
from plexus.main.models import Server, Alias, Location, IPAddress, OSFamily
from plexus.main.models import OperatingSystem, ServerNote, Note
from plexus.main.models import Application, Technology
from plexus.main.models import ApplicationAlias, VMLocation
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from restclient import GET


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self):
        return dict(
            servers=Server.objects.filter(deprecated=False).order_by('name'),
            aliases=(Alias.objects.all().exclude(status='deprecated')
                     .order_by('hostname')),
            applications=Application.objects.all().order_by('name'),
        )


class AddServerView(View):
    template_name = 'main/add_server.html'

    def post(self, request):
        virtual = request.POST.get('virtual', False) == '1'
        location = None
        if not virtual:
            location, created = Location.objects.get_or_create(
                name=request.POST.get("location", "unknown"))
        os_string = request.POST.get("operating_system")
        if ":" not in os_string:
            os_string = "Unknown: " + os_string
        family, version = os_string.split(":")
        os_family, created = OSFamily.objects.get_or_create(name=family)
        operating_system, created = OperatingSystem.objects.get_or_create(
            family=os_family,
            version=version)
        name = request.POST.get('name', 'unknown server')
        graphite_name = request.POST.get('graphite_name', '')
        server = Server.objects.create(
            name=name,
            primary_function=request.POST.get('primary_function', ''),
            virtual=virtual,
            location=location,
            operating_system=operating_system,
            memory=request.POST.get('memory', ''),
            swap=request.POST.get('swap', ''),
            disk=request.POST.get('disk', ''),
            notes=request.POST.get('notes', ''),
            graphite_name=graphite_name,
            sentry_name=request.POST.get('sentry_name', ''),
        )
        if request.POST.get('ip0', False):
            ipv4 = request.POST.get('ip0', '')
            mac = request.POST.get('mac0', '')
            interface, created = IPAddress.objects.get_or_create(
                ipv4=ipv4,
                mac_addr=mac,
                server=server,
            )
        if request.POST.get('ip1', False):
            ipv4 = request.POST.get('ip1', '')
            mac = request.POST.get('mac1', '')
            interface, created = IPAddress.objects.get_or_create(
                ipv4=ipv4,
                mac_addr=mac,
                server=server,
            )
            server.set_contacts(request.POST.get('contact', '').split(','))
        return HttpResponseRedirect("/")

    def get(self, request):
        return render(
            request,
            self.template_name,
            dict(all_locations=Location.objects.all(),
                 all_operating_systems=OperatingSystem.objects.all()))


class AssociateDom0View(View):
    def post(self, request, id):
        server = get_object_or_404(Server, id=id)
        dom0 = get_object_or_404(Server, id=request.POST.get('dom0', '0'))
        VMLocation.objects.create(dom_0=dom0, dom_u=server)
        return HttpResponseRedirect("/server/%d/" % server.id)


class AddAliasView(View):
    def post(self, request, id):
        server = get_object_or_404(Server, id=id)
        ipaddress_id = request.POST.get('ipaddress', None)
        ipaddress = server.ipaddress_default(ipaddress_id)
        alias = Alias.objects.create(
            hostname=request.POST.get('hostname', '[none]'),
            ip_address=ipaddress,
            description=request.POST.get('description', ''),
            administrative_info=request.POST.get('administrative_info', ''),
        )
        alias.set_contacts(request.POST.get('contact', '').split(','))
        return HttpResponseRedirect("/server/%d/" % server.id)


class RequestAliasView(View):
    def post(self, request, id):
        server = get_object_or_404(Server, id=id)
        ipaddress_id = request.POST.get('ipaddress', None)
        ipaddress = server.ipaddress_default(ipaddress_id)
        alias = Alias.objects.create(
            hostname=request.POST.get('hostname', '[none]'),
            ip_address=ipaddress,
            description=request.POST.get('description', ''),
            status='pending',
        )
        alias.set_contacts(request.POST.get('contact', '').split(','))
        subject = alias.dns_request_email_subject()
        body = alias.dns_request_email_body(request.user.first_name)
        send_mail(subject, body, request.user.email,
                  [settings.HOSTMASTER_EMAIL, settings.SYSADMIN_LIST_EMAIL])

        return HttpResponseRedirect("/server/%d/" % server.id)


class RequestAliasChangeView(View):
    def post(self, request, id):
        alias = get_object_or_404(Alias, id=id)
        current_server = alias.ip_address.server
        current_ip_address = alias.ip_address

        new_server_id = request.POST.get('new_server', None)
        new_server = get_object_or_404(Server, id=new_server_id)
        new_ip_address = new_server.ipaddress_set.all()[0]

        alias.ip_address = new_ip_address
        alias.status = "pending"
        alias.save()

        subject = alias.dns_change_request_email_subject()
        body = alias.dns_change_request_email_body(
            current_server, current_ip_address,
            request.user.first_name)
        send_mail(subject, body, request.user.email,
                  [settings.HOSTMASTER_EMAIL, settings.SYSADMIN_LIST_EMAIL])

        return HttpResponseRedirect("/alias/%d/" % alias.id)


class AliasView(DetailView):
    model = Alias

    def get_context_data(self, **kwargs):
        context = super(AliasView, self).get_context_data(**kwargs)
        context['all_applications'] = Application.objects.all()
        context['all_servers'] = Server.objects.all()
        return context


class AliasConfirmView(View):
    def post(self, request, id):
        alias = get_object_or_404(Alias, id=id)
        alias.status = 'active'
        alias.save()
        return HttpResponseRedirect("/alias/%d/" % alias.id)


class AliasDeleteView(DeleteView):
    model = Alias
    success_url = "/"


class AliasAssociateWithApplicationView(View):
    def post(self, request, id):
        alias = get_object_or_404(Alias, id=id)
        application = get_object_or_404(
            Application,
            id=request.POST.get('application', '0'))
        ApplicationAlias.objects.create(alias=alias, application=application)
        return HttpResponseRedirect("/alias/%d/" % alias.id)


class AddApplicationView(View):
    template_name = 'main/add_application.html'

    def post(self, request):
        technology, created = Technology.objects.get_or_create(
            name=request.POST.get("technology", "unknown"))
        name = request.POST.get('name', 'unknown application')
        graphite_name = request.POST.get('graphite_name', '')
        application = Application.objects.create(
            name=name,
            description=request.POST.get('description', ''),
            technology=technology,
            pmt_id=request.POST.get('pmt_id', '') or '0',
            graphite_name=graphite_name,
            sentry_name=request.POST.get('sentry_name', ''),
        )
        application.set_contacts(request.POST.get('contact', '').split(','))
        return HttpResponseRedirect("/")

    def get(self, request):
        return render(
            request,
            self.template_name,
            dict(all_technologies=Technology.objects.all()))


class GraphiteProxyView(View):
    """ cross-domain javascript security prevents us from being able to just
    point cubism.js at the graphite server, so we implement a very rudimentary
    HTTP proxy here """
    def get(self, request):
        graphite_url = (settings.GRAPHITE_BASE + request.META['PATH_INFO']
                        + "?" + request.META['QUERY_STRING'])
        return HttpResponse(GET(graphite_url), content_type="text/plain")


class AddServerNoteView(LoggedInMixin, View):
    def post(self, request, pk):
        server = get_object_or_404(Server, pk=pk)
        n = Note.objects.create(
            user=request.user, body=request.POST.get('body', ''))
        ServerNote.objects.create(
            server=server, note=n)
        return HttpResponseRedirect(server.get_absolute_url())
