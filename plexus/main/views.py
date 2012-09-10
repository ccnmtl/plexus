from annoying.decorators import render_to
from plexus.main.models import Server, Alias, Location, IPAddress, OSFamily
from plexus.main.models import OperatingSystem
from django.http import HttpResponseRedirect

@render_to('main/index.html')
def index(request):
    return dict(servers=Server.objects.all(),
                aliases=Alias.objects.all())

@render_to('main/add_server.html')
def add_server(request):
    if request.method == 'POST':
        virtual = request.POST.get('virtual', False) == '1'
        location = None
        if not virtual:
            location, created = Location.objects.get_or_create(
                name=request.POST.get("location","unknown"))
        os_string = request.POST.get("operating_system")
        family, version = os_string.split(":")
        os_family, created = OSFamily.objects.get_or_create(name=family)
        operating_system, created = OperatingSystem.objects.get_or_create(
            family=os_family,
            version=version)
        server = Server.objects.create(
            name=request.POST.get('name', 'unknown server'),
            primary_function=request.POST.get('primary_function', ''),
            virtual=virtual,
            location=location,
            operating_system=operating_system,
            memory=request.POST.get('memory', ''),
            swap=request.POST.get('swap', ''),
            disk=request.POST.get('disk', ''),
            notes=request.POST.get('notes', ''),
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

        return HttpResponseRedirect("/")
        
    return dict()
