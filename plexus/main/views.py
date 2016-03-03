from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.views.generic import TemplateView, DetailView, DeleteView
from plexus.main.models import (
    Server, Alias, Location, IPAddress, OSFamily,
    OperatingSystem, ServerNote, Note,
    Application, Technology,
    ApplicationAlias, VMLocation,
    ApplicationNote, ServerContact,
)

from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self):
        return dict(
            servers=Server.objects.filter(
                deprecated=False).order_by('name').select_related('location'),
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


class DeleteServerContactView(DeleteView):
    model = ServerContact

    def get_success_url(self):
        return reverse('server-detail', args=[self.object.id])


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

        new_ipaddress_id = request.POST.get('new_ipaddress', None)
        new_ip_address = get_object_or_404(IPAddress, id=new_ipaddress_id)

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
        context['all_servers'] = Server.objects.filter(deprecated=False)
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


class AddServerNoteView(LoggedInMixin, View):
    def post(self, request, pk):
        server = get_object_or_404(Server, pk=pk)
        n = Note.objects.create(
            user=request.user, body=request.POST.get('body', ''))
        ServerNote.objects.create(
            server=server, note=n)
        return HttpResponseRedirect(server.get_absolute_url())


class AddApplicationNoteView(LoggedInMixin, View):
    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        n = Note.objects.create(
            user=request.user, body=request.POST.get('body', ''))
        ApplicationNote.objects.create(
            application=application, note=n)
        return HttpResponseRedirect(application.get_absolute_url())
