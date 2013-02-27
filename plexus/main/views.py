from annoying.decorators import render_to
from django.shortcuts import get_object_or_404
from plexus.main.models import Server, Alias, Location, IPAddress, OSFamily
from plexus.main.models import OperatingSystem, Contact, AliasContact
from plexus.main.models import Application, Technology
from plexus.main.models import ApplicationAlias, VMLocation
from plexus.main.models import ApplicationContact, ServerContact
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from restclient import GET


@render_to('main/index.html')
def index(request):
    return dict(
        servers=Server.objects.filter(deprecated=False).order_by('name'),
        aliases=(Alias.objects.all().exclude(status='deprecated')
                 .order_by('hostname')),
        applications=Application.objects.all().order_by('name'),
    )


@render_to('main/add_server.html')
def add_server(request):
    if request.method == 'POST':
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
        for c in request.POST.get('contact', '').split(','):
            contact, created = Contact.objects.get_or_create(name=c)
            ServerContact.objects.create(server=server,
                                         contact=contact)

        return HttpResponseRedirect("/")
    return dict(all_locations=Location.objects.all(),
                all_operating_systems=OperatingSystem.objects.all())


@render_to("main/server.html")
def server(request, id):
    server = get_object_or_404(Server, id=id)
    return dict(server=server, settings=settings,
                potential_dom0s=(Server.objects.filter(virtual=False)
                                 .exclude(id=server.id))
                )


def associate_dom0(request, id):
    server = get_object_or_404(Server, id=id)
    dom0 = get_object_or_404(Server, id=request.POST.get('dom0', '0'))
    VMLocation.objects.create(dom_0=dom0, dom_u=server)
    return HttpResponseRedirect("/server/%d/" % server.id)


def add_alias(request, id):
    server = get_object_or_404(Server, id=id)
    ipaddress = request.POST.get('ipaddress', None)
    if ipaddress:
        ipaddress = IPAddress.objects.get(id=ipaddress)
    else:
        ipaddress = server.ipaddress_set.all()[0]
    alias = Alias.objects.create(
        hostname=request.POST.get('hostname', '[none]'),
        ip_address=ipaddress,
        description=request.POST.get('description', ''),
    )
    for c in request.POST.get('contact', '').split(','):
        contact, created = Contact.objects.get_or_create(name=c)
        AliasContact.objects.create(alias=alias, contact=contact)

    return HttpResponseRedirect("/server/%d/" % server.id)


def request_alias(request, id):
    server = get_object_or_404(Server, id=id)
    ipaddress = request.POST.get('ipaddress', None)
    if ipaddress:
        ipaddress = IPAddress.objects.get(id=ipaddress)
    else:
        ipaddress = server.ipaddress_set.all()[0]
    alias = Alias.objects.create(
        hostname=request.POST.get('hostname', '[none]'),
        ip_address=ipaddress,
        description=request.POST.get('description', ''),
        status='pending',
    )
    for c in request.POST.get('contact', '').split(','):
        contact, created = Contact.objects.get_or_create(name=c)
        AliasContact.objects.create(alias=alias, contact=contact)

    subject = "DNS Alias Request: " + alias.hostname
    body = """
Please add the following alias:

      %s

It should resolve to %s (%s)

Thanks,
%s
""" % (alias.hostname, server.name, ipaddress.ipv4, request.user.first_name)
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

    subject = "DNS Alias Change Request: " + alias.hostname
    body = """
Please change the following alias:

    %s

Which currently is an alias for %s (%s).

It should be changed to instead point to %s (%s).

Thanks,
%s
""" % (alias.hostname, current_server.name, current_ip_address.ipv4,
       new_server.name, new_ip_address.ipv4,
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


def alias_delete(request, id):
    alias = get_object_or_404(Alias, id=id)
    alias.delete()
    return HttpResponseRedirect("/")


def alias_associate_with_application(request, id):
    alias = get_object_or_404(Alias, id=id)
    application = get_object_or_404(Application,
                                    id=request.POST.get('application', '0'))
    ApplicationAlias.objects.create(alias=alias, application=application)
    return HttpResponseRedirect("/alias/%d/" % alias.id)


@render_to("main/contact.html")
def contact(request, id):
    contact = get_object_or_404(Contact, id=id)
    return dict(contact=contact)


@render_to("main/contact_dashboard.html")
def contact_dashboard(request, id):
    contact = get_object_or_404(Contact, id=id)
    return dict(contact=contact, settings=settings)


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
        for c in request.POST.get('contact', '').split(','):
            contact, created = Contact.objects.get_or_create(name=c)
            ApplicationContact.objects.create(application=application,
                                              contact=contact)
        return HttpResponseRedirect("/")
    return dict(all_technologies=Technology.objects.all())


@render_to('main/application.html')
def application(request, id):
    application = get_object_or_404(Application, id=id)
    return dict(application=application, settings=settings)


@render_to('main/os_family.html')
def os_family(request, id):
    family = get_object_or_404(OSFamily, id=id)
    return dict(family=family)


@render_to('main/os_version.html')
def os_version(request, family_id, id):
    operating_system = get_object_or_404(OperatingSystem, id=id)
    return dict(operating_system=operating_system)


@render_to('main/location.html')
def location(request, id):
    l = get_object_or_404(Location, id=id)
    return dict(location=l)


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
