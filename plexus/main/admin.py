from django.contrib import admin
from plexus.main.models import Location, OSFamily, OperatingSystem, IPAddress
from plexus.main.models import Contact, Alias, Technology
from plexus.main.models import Application, ApplicationAlias, ApplicationContact
from plexus.main.models import ServerContact

for c in [Location, OSFamily, OperatingSystem, IPAddress,
          Contact, Alias, Technology, Application, ApplicationAlias,
          ApplicationContact, ServerContact]:
    admin.site.register(c)
