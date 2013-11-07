from annoying.decorators import render_to
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import TemplateView, DetailView, DeleteView
from plexus.main.models import Server, Alias, Location, IPAddress, OSFamily
from plexus.main.models import OperatingSystem, Contact
from plexus.main.models import Application, Technology
from plexus.main.models import ApplicationAlias, VMLocation
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from restclient import GET


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
            munin_name=request.POST.get('munin_name', ''),
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


class ServerView(DetailView):
    model = Server
    template_name = "main/server.html"
    context_object_name = "server"

    def get_context_data(self, **kwargs):
        return dict(settings=settings, server=kwargs['object'])


def associate_dom0(request, id):
    server = get_object_or_404(Server, id=id)
    dom0 = get_object_or_404(Server, id=request.POST.get('dom0', '0'))
    VMLocation.objects.create(dom_0=dom0, dom_u=server)
    return HttpResponseRedirect("/server/%d/" % server.id)


def add_alias(request, id):
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


def request_alias(request, id):
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
    body = alias.dns_request_body(request.user.first_name)
    send_mail(subject, body, request.user.email,
              [settings.HOSTMASTER_EMAIL, settings.SYSADMIN_LIST_EMAIL])

    return HttpResponseRedirect("/server/%d/" % server.id)


def request_alias_change(request, id):
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


@render_to("main/alias.html")
def alias(request, id):
    alias = get_object_or_404(Alias, id=id)
    return dict(alias=alias,
                all_applications=Application.objects.all(),
                all_servers=Server.objects.all(),
                )


def alias_confirm(request, id):
    alias = get_object_or_404(Alias, id=id)
    alias.status = 'active'
    alias.save()
    return HttpResponseRedirect("/alias/%d/" % alias.id)


class AliasDeleteView(DeleteView):
    model = Alias
    success_url = "/"


def alias_associate_with_application(request, id):
    alias = get_object_or_404(Alias, id=id)
    application = get_object_or_404(Application,
                                    id=request.POST.get('application', '0'))
    ApplicationAlias.objects.create(alias=alias, application=application)
    return HttpResponseRedirect("/alias/%d/" % alias.id)


class ContactView(DetailView):
    template_name = "main/contact.html"
    model = Contact
    context_object_name = "contact"


@render_to('main/add_application.html')
def add_application(request):
    if request.method == 'POST':
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
    return dict(all_technologies=Technology.objects.all())


class ApplicationView(DetailView):
    template_name = 'main/application.html'
    model = Application
    context_object_name = "application"


class OSFamilyView(DetailView):
    template_name = 'main/os_family.html'
    model = OSFamily
    context_object_name = "family"


class OSVersionView(DetailView):
    template_name = 'main/os_version.html'
    model = OperatingSystem
    context_object_name = "operating_system"


class LocationView(DetailView):
    template_name = 'main/location.html'
    model = Location
    context_object_name = "location"


def render_proxy(request):
    """ cross-domain javascript security prevents us from being able to just
    point cubism.js at the graphite server, so we implement a very rudimentary
    HTTP proxy here """
    graphite_url = (settings.GRAPHITE_BASE + request.META['PATH_INFO']
                    + "?" + request.META['QUERY_STRING'])
    return HttpResponse(GET(graphite_url), content_type="text/plain")


def metrics_proxy(request):
    graphite_url = (settings.GRAPHITE_BASE + request.META['PATH_INFO']
                    + "?" + request.META['QUERY_STRING'])
    return HttpResponse(GET(graphite_url), content_type="text/plain")
