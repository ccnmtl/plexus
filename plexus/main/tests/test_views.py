from django.test import TestCase
from django.test.utils import override_settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from .factories import ServerFactory, IPAddressFactory, ContactFactory
from .factories import ApplicationFactory, AliasFactory
import httpretty
from django.test.client import Client
from plexus.main.models import Server
from plexus.main.models import Contact
from plexus.main.models import OSFamily, Alias
from plexus.main.models import OperatingSystem
from plexus.main.models import Location
from plexus.main.models import VMLocation
from plexus.main.models import ServerNote, Note, ApplicationNote


class SimpleTest(TestCase):
    def setUp(self):
        self.c = Client()

    def tearDown(self):
        pass

    def test_root(self):
        response = self.c.get("/")
        self.assertEquals(response.status_code, 200)

    def test_smoketest(self):
        """ just run the smoketests. we don't care if they pass/fail """
        response = self.c.get("/smoketest/")
        self.assertEquals(response.status_code, 200)

    def test_add_server_form(self):
        response = self.c.get("/add_server/")
        self.assertEquals(response.status_code, 200)

    def test_add_application_form(self):
        response = self.c.get("/add_application/")
        self.assertEquals(response.status_code, 200)

    def test_add_application(self):
        response = self.c.post(
            "/add_application/",
            dict(
                name="testapp",
                description="application for testing",
                technology="Erlang",
                graphite_name="testapp",
            )
        )
        self.assertEqual(response.status_code, 302)
        response = self.c.get("/")
        self.assertTrue("testapp" in response.content)

    def test_add_server(self):
        response = self.c.post(
            "/add_server/",
            {
                'virtual': '0',
                'location': 'test location',
                'operating_system': 'Linux: Ubuntu 12.04',
                'name': 'testserver',
                'ip0': '127.0.0.1',
                'mac0': '00:00:00:00:00:00',
                'ip1': '127.0.0.2',
                'mac1': '00:00:00:00:00:01',
                'contact': 'Anders,Jonah',
            })
        self.assertEquals(response.status_code, 302)
        response = self.c.get("/")
        assert "testserver" in response.content

        # pull up the server page
        s = Server.objects.get(name='testserver')
        response = self.c.get(s.get_absolute_url())

        self.assertEquals(response.status_code, 200)
        assert '127.0.0.1' in response.content
        assert 'Anders' in response.content

        l = Location.objects.get(name="test location")
        response = self.c.get(l.get_absolute_url())
        self.assertEquals(response.status_code, 200)
        assert 'testserver' in response.content

        # contacts should exist too
        c = Contact.objects.get(name="Anders")
        response = self.c.get(c.get_absolute_url())
        self.assertEquals(response.status_code, 200)
        assert 'Anders' in response.content
        assert 'testserver' in response.content

        # os info should exist now
        osfam = OSFamily.objects.get(name="Linux")
        response = self.c.get(osfam.get_absolute_url())
        assert response.status_code == 200
        assert "Ubuntu 12.04" in response.content
        os = OperatingSystem.objects.get(family=osfam, version=" Ubuntu 12.04")
        response = self.c.get(os.get_absolute_url())
        assert response.status_code == 200
        assert "testserver" in response.content

    def test_add_server_alternates(self):
        response = self.c.post(
            "/add_server/",
            {
                'virtual': '1',
                'location': 'test location',
                'operating_system': 'Foobar',
                'name': 'testserver',
                'contact': 'Anders,Jonah',
            })
        self.assertEquals(response.status_code, 302)
        response = self.c.get("/")
        assert "testserver" in response.content

    def test_add_alias(self):
        server = ServerFactory()
        IPAddressFactory(server=server)

        response = self.c.post(
            "/server/%d/add_alias/" % server.id,
            {
                'hostname': 'test.example.com',
                'description': 'a description',
                'administrative_info': 'admin info',
                'contact': 'Anders,Jonah',
            })
        self.assertEquals(response.status_code, 302)
        response = self.c.get("/server/%d/" % server.id)
        assert "test.example.com" in response.content

        a = Alias.objects.get(hostname='test.example.com')
        response = self.c.get("/alias/%d/" % a.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("admin info" in response.content)

    def test_contact(self):
        contact = ContactFactory()
        response = self.c.get("/contact/%d/" % contact.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['contact'], contact)

    def test_contact_dashboard(self):
        contact = ContactFactory()
        response = self.c.get("/contact/%d/dashboard/" % contact.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['contact'], contact)

    def test_application(self):
        application = ApplicationFactory()
        response = self.c.get("/application/%d/" % application.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['application'], application)

    def test_delete_alias(self):
        alias = AliasFactory()
        response = self.c.get("/alias/%d/delete/" % alias.id)
        self.assertEqual(response.status_code, 200)
        # should just be a confirmation
        self.assertEqual(Alias.objects.count(), 1)
        response = self.c.post("/alias/%d/delete/" % alias.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Alias.objects.count(), 0)

    def test_associate_dom0(self):
        s1 = ServerFactory()
        s2 = ServerFactory()
        response = self.c.post(
            "/server/%d/associate_dom0/" % s1.id,
            dict(dom0=s2.id))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(VMLocation.objects.count(), 1)

    def test_alias_confirm(self):
        alias = AliasFactory(status="pending")
        response = self.c.post("/alias/%d/confirm/" % alias.id)
        self.assertEqual(response.status_code, 302)
        response = self.c.get("/alias/%d/" % alias.id)
        self.assertTrue("pending" not in response.content)

    def test_alias_edit_form(self):
        alias = AliasFactory(status="pending")
        response = self.c.get("/alias/%d/edit/" % alias.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("<form " in response.content)
        response = self.c.post(
            "/alias/%d/edit/" % alias.id,
            dict(hostname=alias.hostname,
                 status="active",
                 description="new description",
                 administrative_info="new admin info"),
        )
        self.assertEqual(response.status_code, 302)
        response = self.c.get("/alias/%d/" % alias.id)
        self.assertTrue("new description" in response.content)
        self.assertTrue("new admin info" in response.content)

    def test_alias_associate_with_application(self):
        alias = AliasFactory()
        application = ApplicationFactory()
        response = self.c.post(
            "/alias/%d/associate_with_application/" % alias.id,
            dict(application=application.id))
        self.assertEqual(response.status_code, 302)


class DashboardTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_empty_500s(self):
        response = self.c.get("/dashboard/500s/")
        self.assertEquals(response.status_code, 200)

    def test_500s(self):
        ApplicationFactory(graphite_name='foo')
        response = self.c.get("/dashboard/500s/")
        self.assertEquals(response.status_code, 200)

    def test_empty_traffic(self):
        response = self.c.get("/dashboard/traffic/")
        self.assertEquals(response.status_code, 200)

    def test_traffic(self):
        ApplicationFactory(graphite_name='foo')
        response = self.c.get("/dashboard/traffic/")
        self.assertEquals(response.status_code, 200)


class LoggedInTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create(username="foo", first_name="first",
                                        last_name="last")
        self.user.set_password("test")
        self.user.save()
        self.c.login(username="foo", password="test")

    def test_request_alias(self):
        server = ServerFactory()
        IPAddressFactory(server=server)

        response = self.c.post(
            "/server/%d/request_alias/" % server.id,
            {
                'hostname': 'test.example.com',
                'description': 'a description',
                'administrative_info': 'admin info',
                'contact': 'Anders,Jonah',
            })
        self.assertEquals(response.status_code, 302)
        response = self.c.get("/server/%d/" % server.id)
        assert "test.example.com" in response.content

        a = Alias.objects.get(hostname='test.example.com')
        response = self.c.get("/alias/%d/" % a.id)
        self.assertEqual(response.status_code, 200)

    def test_request_alias_change(self):
        server = ServerFactory()
        ipaddress = IPAddressFactory(server=server)
        alias = AliasFactory(ip_address=ipaddress)
        newipaddress = IPAddressFactory()
        newserver = newipaddress.server

        response = self.c.post(
            "/alias/%d/request_alias_change/" % alias.id,
            {
                'new_server': newserver.id,
            })
        self.assertEquals(response.status_code, 302)
        response = self.c.get("/alias/%d/" % alias.id)
        assert "pending" in response.content

    def test_add_server_note(self):
        server = ServerFactory()
        response = self.c.post(
            reverse("add-server-note", args=(server.id,)),
            {"body": "this is a note"}
        )
        self.assertEquals(response.status_code, 302)
        self.assertEqual(ServerNote.objects.count(), 1)
        self.assertEqual(Note.objects.count(), 1)

    def test_add_application_note(self):
        a = ApplicationFactory()
        response = self.c.post(
            reverse("add-application-note", args=(a.id,)),
            {"body": "this is a note"}
        )
        self.assertEquals(response.status_code, 302)
        self.assertEqual(ApplicationNote.objects.count(), 1)
        self.assertEqual(Note.objects.count(), 1)


class ProxyTests(TestCase):
    def setUp(self):
        self.c = Client()

    @override_settings(GRAPHITE_BASE="http://mock.example.com")
    def test_render_proxy(self):
        httpretty.enable()
        httpretty.register_uri(
            httpretty.GET,
            "http://mock.example.com/render/?foo=bar",
            body="success",
        )
        response = self.c.get("/render/?foo=bar")
        self.assertEqual(response.content, "success")
        httpretty.disable()
        httpretty.reset()

    @override_settings(GRAPHITE_BASE="http://mock.example.com")
    def test_metric_proxy(self):
        httpretty.enable()
        httpretty.register_uri(
            httpretty.GET,
            "http://mock.example.com/metrics/?foo=bar",
            body="success",
        )
        response = self.c.get("/metrics/?foo=bar")
        self.assertEqual(response.content, "success")
        httpretty.disable()
        httpretty.reset()
