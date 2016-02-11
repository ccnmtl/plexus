from django.db import models


MAX_LOGS = 10  # convert this to a django setting later


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
        for gl in self.all()[MAX_LOGS:]:
            gl.delete()


class GrainLog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sha1 = models.TextField(blank=True, default='', db_index=True)
    payload = models.TextField(blank=True, default='')

    objects = GrainLogManager()

    class Meta:
        ordering = ['-created']
