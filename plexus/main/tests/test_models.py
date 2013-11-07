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

    def test_pmt_feed_url(self):
        a = ApplicationFactory()
        self.assertEqual(
            a.pmt_feed_url(),
            "http://pmt.ccnmtl.columbia.edu/project_feed.pl?pid=123")

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
