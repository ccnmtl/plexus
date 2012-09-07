from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=256)
    details = models.TextField(blank=True, default=u"")


class OSFamily(models.Model):
    name = models.CharField(max_length=256)


class OperatingSystem(models.Model):
    family = models.ForeignKey(OSFamily)
    version = models.CharField(max_length=256)


class Server(models.Model):
    name = models.CharField(max_length=256)
    primary_function = models.TextField(blank=True, default=u"")
    virtual = models.BooleanField()
    location = models.ForeignKey(Location)
    operating_system = models.ForeignKey(OperatingSystem)
    memory = models.CharField(max_length=256)
    disk = models.CharField(max_length=256)
    swap = models.CharField(max_length=256)
    notes = models.TextField(blank=True, default=u"")
    deprecated = models.BooleanField(default=False)


class IPAddress(models.Model):
    ipv4 = models.CharField(max_length=256)
    mac_addr = models.CharField(max_length=256)
    server = models.ForeignKey(Server)


class VMLocation(models.Model):
    dom_u = models.ForeignKey(Server, related_name='dom_u')
    dom_0 = models.ForeignKey(Server, related_name='dom_0')


class Contact(models.Model):
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    phone = models.CharField(max_length=256)


class Alias(models.Model):
    hostname = models.CharField(max_length=256)
    ip_address = models.ForeignKey(IPAddress, null=True)
    status = models.CharField(max_length=256, default=u"active")
    description = models.TextField(blank=True, default=u"")


class AliasContact(models.Model):
    alias = models.ForeignKey(Alias)
    contact = models.ForeignKey(Contact)

    class Meta:
        order_with_respect_to = 'alias'
