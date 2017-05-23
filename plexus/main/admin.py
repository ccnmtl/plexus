from models import Location, OSFamily, OperatingSystem, IPAddress
from models import Contact, Alias, Technology
from models import Application, ApplicationAlias, ApplicationContact
from models import ServerContact
from django.contrib import admin

for c in [Location, OSFamily, OperatingSystem, IPAddress,
          Contact, Alias, Technology, Application, ApplicationAlias,
          ApplicationContact, ServerContact]:
    admin.site.register(c)
