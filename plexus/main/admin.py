from models import Location, OSFamily, OperatingSystem, Server, IPAddress
from models import Contact, Alias, AliasContact, Technology
from models import Application, ApplicationAlias, ApplicationContact
from models import ServerContact
from django.contrib import admin

for c in [Location, OSFamily, OperatingSystem, Server, IPAddress,
          Contact, Alias, AliasContact, Technology,
          Application, ApplicationAlias, ApplicationContact,
          ServerContact]:
    admin.site.register(c)
