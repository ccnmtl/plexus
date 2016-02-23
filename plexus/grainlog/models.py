import json

from django.db import models
from django.conf import settings

from .grain import Grain


class GrainLogManager(models.Manager):
    def create_grainlog(self, sha1, payload=""):
        """ create new one. return it (or an existing one)

        but don't enter duplicates (in a row) and don't allow more than
        MAX entries total (deleting oldest to make room)"""
        r = self.all()
        if r.exists() and r.first().sha1 == sha1:
            # don't duplicate the most recent
            return r.first()

        gl = GrainLog(sha1=sha1, payload=payload)
        gl.save()
        self.limit_entries()
        return gl

    def limit_entries(self):
        for gl in self.all()[settings.MAX_GRAINLOGS:]:
            gl.delete()


class GrainLog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sha1 = models.TextField(blank=True, default='', db_index=True)
    payload = models.TextField(blank=True, default='')

    objects = GrainLogManager()

    class Meta:
        ordering = ['-created']
        get_latest_by = 'created'

    def data(self):
        return json.loads(self.payload)

    def grain(self):
        return Grain(d=self.data())


def current_grainlog():
    try:
        return GrainLog.objects.latest()
    except GrainLog.DoesNotExist:
        return None
