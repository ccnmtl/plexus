from django.contrib import admin

from plexus.main.models import (
    Application, ApplicationAlias, ApplicationContact,
    Contact, Alias, Technology, Note,
    Location, IPAddress,
    ServerContact, Server
)


for c in [Location, IPAddress,
          Contact, Technology, Application, ApplicationAlias,
          ApplicationContact, ServerContact, Server, Note]:
    admin.site.register(c)


@admin.register(Alias)
class AliasAdmin(admin.ModelAdmin):
    class Meta:
        model = Alias

    list_display = ("hostname", "status")
