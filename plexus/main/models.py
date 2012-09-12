from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=256)
    details = models.TextField(blank=True, default=u"")

    def __unicode__(self):
        return self.name


class OSFamily(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name


class OperatingSystem(models.Model):
    family = models.ForeignKey(OSFamily)
    version = models.CharField(max_length=256)

    def __unicode__(self):
        return unicode(self.family) + " " + self.version


class Server(models.Model):
    name = models.CharField(max_length=256)
    primary_function = models.TextField(blank=True, default=u"")
    virtual = models.BooleanField()
    location = models.ForeignKey(Location, null=True, default="")
    operating_system = models.ForeignKey(OperatingSystem)
    memory = models.CharField(max_length=256, blank=True)
    disk = models.CharField(max_length=256, blank=True)
    swap = models.CharField(max_length=256, blank=True)
    notes = models.TextField(blank=True, default=u"")
    deprecated = models.BooleanField(default=False)
    graphite_name = models.CharField(max_length=256, default=u"", blank=True)

    def __unicode__(self):
        return self.name


class IPAddress(models.Model):
    ipv4 = models.CharField(max_length=256)
    mac_addr = models.CharField(max_length=256)
    server = models.ForeignKey(Server)

    def __unicode__(self):
        return self.ipv4


class VMLocation(models.Model):
    dom_u = models.ForeignKey(Server, related_name='dom_u')
    dom_0 = models.ForeignKey(Server, related_name='dom_0')

    def __unicode__(self):
        return unicode(self.dom_u)


class Contact(models.Model):
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256, default="")
    phone = models.CharField(max_length=256, default="")

    def __unicode__(self):
        return self.name


class Alias(models.Model):
    hostname = models.CharField(max_length=256)
    ip_address = models.ForeignKey(IPAddress, null=True)
    status = models.CharField(max_length=256, default=u"active")
    description = models.TextField(blank=True, default=u"")

    def __unicode__(self):
        return self.hostname

    def status_css_class(self):
        if self.status == 'pending':
            return "warning"
        if self.status == 'deprecated':
            return "error"
        return ""


class AliasContact(models.Model):
    alias = models.ForeignKey(Alias)
    contact = models.ForeignKey(Contact)

    class Meta:
        order_with_respect_to = 'alias'

    def __unicode__(self):
        return unicode(self.alias) + ": " + unicode(self.contact)


class Technology(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, default=u"")
    technology = models.ForeignKey(Technology, null=True)
    graphite_name = models.CharField(max_length=256, default=u"", blank=True)
    pmt_id = models.IntegerField(default=0)
    # rolf
    # contacts
    # code repos
    # renewals

    def __unicode__(self):
        return self.name


class ApplicationAlias(models.Model):
    application = models.ForeignKey(Application)
    alias = models.ForeignKey(Alias)

    def __unicode__(self):
        return unicode(self.application) + " -> " + unicode(self.alias)
