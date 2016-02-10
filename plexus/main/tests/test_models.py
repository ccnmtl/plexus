from django.test import TestCase
from .factories import LocationFactory, OSFamilyFactory, AliasFactory
from .factories import OperatingSystemFactory, ServerFactory, IPAddressFactory
from .factories import ContactFactory, AliasContactFactory, VMLocationFactory
from .factories import TechnologyFactory, ApplicationFactory
from .factories import ApplicationAliasFactory, ApplicationContactFactory
from .factories import ServerContactFactory


class BasicTest(TestCase):
    def test_unicode(self):
        self.assertEquals(str(LocationFactory()), "test")
        self.assertEquals(str(OSFamilyFactory()), "test os family")
        self.assertEquals(str(OperatingSystemFactory()), "test os family 1.0")
        self.assertEquals(str(ServerFactory()), "test server")
        self.assertEquals(str(IPAddressFactory()), "127.0.0.1")
        self.assertEquals(str(VMLocationFactory()), "test server")
        self.assertEquals(str(ContactFactory()), "anders")


class AliasTest(TestCase):
    def test_unicode(self):
        self.assertEquals(str(AliasFactory()), "foo.example.com")

    def test_css_status(self):
        alias = AliasFactory()
        self.assertEquals(alias.status_css_class(), "")
        alias.status = "pending"
        self.assertEquals(alias.status_css_class(), "warning")
        alias.status = "deprecated"
        self.assertEquals(alias.status_css_class(), "error")

    def test_is_deprecated(self):
        alias = AliasFactory(status='deprecated')
        self.assertTrue(alias.is_deprecated())
        alias = AliasFactory(status='pending')
        self.assertFalse(alias.is_deprecated())

    def test_can_request(self):
        self.assertFalse(AliasFactory().can_request_dns_change())

    def test_dns_change_request_email_subject(self):
        a = AliasFactory()
        self.assertEqual(
            a.dns_change_request_email_subject(),
            "DNS Alias Change Request: foo.example.com")

    def test_dns_request_email_subject(self):
        a = AliasFactory()
        self.assertEqual(
            a.dns_request_email_subject(),
            "DNS Alias Request: foo.example.com")

    def test_dns_request_email_body(self):
        a = AliasFactory()
        self.assertEqual(
            a.dns_request_email_body("Anders"),
            """
Please add the following alias:

      foo.example.com

It should resolve to test server (127.0.0.1)

Thanks,
Anders
""")

    def test_dns_change_request_email_body(self):
        a = AliasFactory()
        current_server = ServerFactory(name="current")
        current_ipaddr = IPAddressFactory(
            server=current_server,
            ipv4="127.0.0.2")
        self.assertEqual(
            a.dns_change_request_email_body(
                current_server, current_ipaddr, "Anders"),
            """
Please change the following alias:

    foo.example.com

Which currently is an alias for current (127.0.0.2).

It should be changed to instead point to test server (127.0.0.1).

Thanks,
Anders
""")

    def test_add_contacts(self):
        a = AliasFactory()
        self.assertEqual(a.aliascontact_set.count(), 0)
        a.add_contacts(['One', 'Two', 'Three'])
        self.assertEqual(a.aliascontact_set.count(), 3)

    def test_set_contacts(self):
        a = AliasFactory()
        # start with none
        self.assertEqual(a.aliascontact_set.count(), 0)
        # set it to three
        a.set_contacts(['One', 'Two', 'Three'])
        self.assertEqual(a.aliascontact_set.count(), 3)
        # repeating shouldn't change that
        a.set_contacts(['One', 'Two', 'Three'])
        self.assertEqual(a.aliascontact_set.count(), 3)
        # but we should be able to add/remove
        a.set_contacts(['Three', 'Four'])
        self.assertEqual(a.aliascontact_set.count(), 2)

    def test_get_absolute_url(self):
        a = AliasFactory()
        self.assertEqual(a.get_absolute_url(), "/alias/%d/" % a.id)


class AliasContactTest(TestCase):
    def test_unicode(self):
        ac = AliasContactFactory()
        self.assertEqual(str(ac), "foo.example.com: anders")


class TechnologyTest(TestCase):
    def test_unicode(self):
        t = TechnologyFactory()
        self.assertEqual(str(t), "Django")


class ApplicationTest(TestCase):
    def test_unicode(self):
        a = ApplicationFactory()
        self.assertEqual(str(a), "Test Application")

    def test_get_absolute_url(self):
        a = ApplicationFactory()
        self.assertEqual(a.get_absolute_url(), "/application/%d/" % a.id)

    def test_pmt_feed_url(self):
        a = ApplicationFactory()
        self.assertEqual(
            a.pmt_feed_url(),
            "https://pmt.ccnmtl.columbia.edu/feeds/project/123/")

    def test_add_contacts(self):
        a = ApplicationFactory()
        self.assertEqual(a.applicationcontact_set.count(), 0)
        a.add_contacts(['One', 'Two', 'Three'])
        self.assertEqual(a.applicationcontact_set.count(), 3)

    def test_set_contacts(self):
        a = ApplicationFactory()
        # start with none
        self.assertEqual(a.applicationcontact_set.count(), 0)
        # set it to three
        a.set_contacts(['One', 'Two', 'Three'])
        self.assertEqual(a.applicationcontact_set.count(), 3)
        # repeating shouldn't change that
        a.set_contacts(['One', 'Two', 'Three'])
        self.assertEqual(a.applicationcontact_set.count(), 3)
        # but we should be able to add/remove
        a.set_contacts(['Three', 'Four'])
        self.assertEqual(a.applicationcontact_set.count(), 2)

    def test_application_notes_empty(self):
        a = ApplicationFactory()
        self.assertEqual(len(a.application_notes()), 0)


class ApplicationAliasTest(TestCase):
    def test_unicode(self):
        a = ApplicationAliasFactory()
        self.assertEqual(str(a), "Test Application -> foo.example.com")


class ApplicationContactTest(TestCase):
    def test_unicode(self):
        a = ApplicationContactFactory()
        self.assertEqual(str(a), "Test Application: anders")


class ServerContactTest(TestCase):
    def test_unicode(self):
        a = ServerContactFactory()
        self.assertEqual(str(a), "test server: anders")


class ServerTest(TestCase):
    def test_add_contacts(self):
        a = ServerFactory()
        self.assertEqual(a.servercontact_set.count(), 0)
        a.add_contacts(['One', 'Two', 'Three'])
        self.assertEqual(a.servercontact_set.count(), 3)

    def test_set_contacts(self):
        a = ServerFactory()
        # start with none
        self.assertEqual(a.servercontact_set.count(), 0)
        # set it to three
        a.set_contacts(['One', 'Two', 'Three'])
        self.assertEqual(a.servercontact_set.count(), 3)
        # repeating shouldn't change that
        a.set_contacts(['One', 'Two', 'Three'])
        self.assertEqual(a.servercontact_set.count(), 3)
        # but we should be able to add/remove
        a.set_contacts(['Three', 'Four'])
        self.assertEqual(a.servercontact_set.count(), 2)

    def test_ipaddress_default(self):
        ipaddress = IPAddressFactory()
        i = ipaddress.server.ipaddress_default(None)
        self.assertEqual(ipaddress, i)
        i2 = ipaddress.server.ipaddress_default(ipaddress.id)
        self.assertEqual(ipaddress, i2)

    def test_potential_dom0s(self):
        s = ServerFactory()
        self.assertEqual(s.potential_dom0s().count(), 0)

    def test_server_notes_empty(self):
        s = ServerFactory()
        self.assertEqual(len(s.server_notes()), 0)
