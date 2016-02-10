from django.db import models


class GrainLog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sha1 = models.TextField(blank=True, default='', db_index=True)
    payload = models.TextField(blank=True, default='')
