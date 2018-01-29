from django.contrib import admin

from models import Application, ApplicationAlias, ApplicationContact
from models import Contact, Alias, Technology
from models import Location, OSFamily, OperatingSystem, IPAddress
from models import ServerContact
from plexus.main.models import Server


for c in [Location, OSFamily, OperatingSystem, IPAddress,
          Contact, Alias, Technology, Application, ApplicationAlias,
          ApplicationContact, ServerContact, Server]:
    admin.site.register(c)
