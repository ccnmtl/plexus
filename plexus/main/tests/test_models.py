from django.test import TestCase
from .factories import LocationFactory, OSFamilyFactory, AliasFactory
from .factories import OperatingSystemFactory, ServerFactory, IPAddressFactory
from .factories import ContactFactory, AliasContactFactory, VMLocationFactory


class BasicTest(TestCase):
    def test_unicode(self):
        self.assertEquals(str(LocationFactory()), "test")
        self.assertEquals(str(OSFamilyFactory()), "test os family")
        self.assertEquals(str(OperatingSystemFactory()), "test os family 1.0")
        self.assertEquals(str(ServerFactory()), "test server")
        self.assertEquals(str(IPAddressFactory()), "127.0.0.1")
        self.assertEquals(str(AliasFactory()), "foo.example.com")
        self.assertEquals(str(VMLocationFactory()), "test server")
        self.assertEquals(str(ContactFactory()), "anders")

    def test_css_status(self):
        alias = AliasFactory()
        self.assertEquals(alias.status_css_class(), "")
        alias.status = "pending"
        self.assertEquals(alias.status_css_class(), "warning")
        alias.status = "deprecated"
        self.assertEquals(alias.status_css_class(), "error")

    def test_can_request(self):
        self.assertFalse(AliasFactory().can_request_dns_change())


class AliasContactTest(TestCase):
    def test_unicode(self):
        ac = AliasContactFactory()
        self.assertEqual(str(ac), "foo.example.com: anders")
