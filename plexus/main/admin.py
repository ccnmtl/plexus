from models import Location, OSFamily, OperatingSystem, Server, IPAddress
from models import VMLocation, Contact, Alias, AliasContact, Technology
from models import Application
from django.contrib import admin

for c in [Location, OSFamily, OperatingSystem, Server, IPAddress,
          VMLocation, Contact, Alias, AliasContact, Technology,
          Application]:
    admin.site.register(c)
