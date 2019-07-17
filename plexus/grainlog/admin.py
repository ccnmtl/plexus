from django.contrib import admin
from plexus.grainlog.models import GrainLog


@admin.register(GrainLog)
class GrainLogAdmin(admin.ModelAdmin):
    class Meta:
        model = GrainLog

    list_display = ('sha1', 'created')
