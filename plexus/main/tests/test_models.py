from django.test import TestCase
from plexus.main.models import Location
from plexus.main.models import OSFamily
from plexus.main.models import OperatingSystem
from plexus.main.models import IPAddress
from plexus.main.models import Server
from plexus.main.models import Alias


class BasicTest(TestCase):
    def setUp(self):
        self.l = Location.objects.create(
            name="test",
            details="test location")
        self.osfam = OSFamily.objects.create(
            name="test os family")
        self.os = OperatingSystem.objects.create(
            family=self.osfam,
            version="1.0",
            )
        self.server = Server.objects.create(
            name="test server",
            virtual=False,
            location=self.l,
            operating_system=self.os,
            )
        self.ipaddr = IPAddress.objects.create(
            ipv4="127.0.0.1",
            mac_addr="00:16:3e:e3:61:53",
            server=self.server,
            )
        self.alias = Alias.objects.create(
            hostname="foo.example.com",
            ip_address=self.ipaddr,
            status="active",
            )


    def tearDown(self):
        self.l.delete()
        self.osfam.delete()
        self.os.delete()
        self.server.delete()
        self.ipaddr.delete()
        self.alias.delete()

    def test_unicode(self):
        self.assertEquals(str(self.l), "test")
        self.assertEquals(str(self.osfam), "test os family")
        self.assertEquals(str(self.os), "test os family 1.0")
        self.assertEquals(str(self.server), "test server")
        self.assertEquals(str(self.ipaddr), "127.0.0.1")
        self.assertEquals(str(self.alias), "foo.example.com")

    def test_css_status(self):
        self.assertEquals(self.alias.status_css_class(), "")
