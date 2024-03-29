from django.urls import reverse
from django.test import TestCase
from django.test.client import Client

from plexus.main.models import (
    Server, ServerContact, Contact, Alias,
    Location, ServerNote, Note,
    ApplicationNote, ApplicationContact, Lease)
from plexus.main.tests.factories import UserFactory

from plexus.main.tests.factories import (
    ServerFactory, IPAddressFactory, ContactFactory,
    ApplicationFactory, AliasFactory, ServerContactFactory,
    ApplicationContactFactory)


class SimpleTest(TestCase):
    def setUp(self):
        self.c = Client()

    def tearDown(self):
        pass

    def test_root(self):
        response = self.c.get("/")
        self.assertEqual(response.status_code, 302)

    def test_smoketest(self):
        """ just run the smoketests. we don't care if they pass/fail """
        self.c.get("/smoketest/")


class DashboardTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = UserFactory()
        self.c.login(username=self.user.username, password="test")

    def test_empty_500s(self):
        response = self.c.get(reverse('500s-dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_500s(self):
        ApplicationFactory(graphite_name='foo')
        response = self.c.get(reverse('500s-dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_500s_deprecated_app(self):
        ApplicationFactory(graphite_name='foobar', deprecated=True)
        response = self.c.get(reverse('500s-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'foobar')

    def test_empty_404s(self):
        response = self.c.get(reverse('404s-dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_404s(self):
        ApplicationFactory(graphite_name='foo')
        response = self.c.get(reverse('404s-dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_404s_deprecated_app(self):
        ApplicationFactory(graphite_name='foobar', deprecated=True)
        response = self.c.get(reverse('404s-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'foobar')

    def test_empty_traffic(self):
        response = self.c.get(reverse('traffic-dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_traffic(self):
        ApplicationFactory(graphite_name='foo')
        response = self.c.get(reverse('traffic-dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_traffic_deprecated_app(self):
        ApplicationFactory(graphite_name='foobar', deprecated=True)
        response = self.c.get(reverse('traffic-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'foobar')

    def test_empty_response_times(self):
        response = self.c.get(reverse('response-time-dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_response_times(self):
        ApplicationFactory(graphite_name='foo')
        response = self.c.get(reverse('response-time-dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_response_times_deprecated_app(self):
        ApplicationFactory(graphite_name='foobar', deprecated=True)
        response = self.c.get(reverse('response-time-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'foobar')

    def test_load_average_empty(self):
        response = self.c.get(reverse('load-dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_load_average(self):
        ServerFactory(graphite_name='foo')
        response = self.c.get(reverse('load-dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_network_empty(self):
        response = self.c.get(reverse('network-dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_network(self):
        ServerFactory(graphite_name='foo')
        response = self.c.get(reverse('network-dashboard'))
        self.assertEqual(response.status_code, 200)


class LoggedInTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = UserFactory()
        self.c.login(username=self.user.username, password="test")

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
        self.assertEqual(response.status_code, 302)
        response = self.c.get("/server/%d/" % server.id)
        self.assertContains(response, 'test.example.com')

        a = Alias.objects.get(hostname='test.example.com')
        response = self.c.get("/alias/%d/" % a.id)
        self.assertEqual(response.status_code, 200)

    def test_request_alias_change(self):
        server = ServerFactory()
        ipaddress = IPAddressFactory(server=server)
        alias = AliasFactory(ip_address=ipaddress)
        newipaddress = IPAddressFactory()

        response = self.c.post(
            "/alias/%d/request_alias_change/" % alias.id,
            {
                'new_ipaddress': newipaddress.id,
            })
        self.assertEqual(response.status_code, 302)
        response = self.c.get("/alias/%d/" % alias.id)
        self.assertContains(response, 'pending')

    def test_alias_change(self):
        server = ServerFactory()
        ipaddress = IPAddressFactory(server=server)
        alias = AliasFactory(ip_address=ipaddress)
        newipaddress = IPAddressFactory()

        response = self.c.post(
            reverse('alias-change', args=[alias.id]),
            {
                'new_ipaddress': newipaddress.id,
            })
        self.assertEqual(response.status_code, 302)
        response = self.c.get("/alias/%d/" % alias.id)
        self.assertContains(response, newipaddress.server.name)

    def test_add_server_note(self):
        server = ServerFactory()
        response = self.c.post(
            reverse("add-server-note", args=(server.id,)),
            {"body": "this is a note"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ServerNote.objects.count(), 1)
        self.assertEqual(Note.objects.count(), 1)

    def test_add_server_contact(self):
        server = ServerFactory()
        response = self.c.post(
            reverse("add-server-contact", args=(server.id,)),
            {"contact": "ContactBob"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ServerContact.objects.count(), 1)
        contact = ServerContact.objects.first()
        self.assertEqual(contact.contact.name, 'ContactBob')
        self.assertEqual(contact.server, server)

    def test_add_application_note(self):
        a = ApplicationFactory()
        response = self.c.post(
            reverse("add-application-note", args=(a.id,)),
            {"body": "this is a note"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ApplicationNote.objects.count(), 1)
        self.assertEqual(Note.objects.count(), 1)

    def test_add_application_contact(self):
        a = ApplicationFactory()
        response = self.c.post(
            reverse("add-application-contact", args=(a.id,)),
            {"contact": "ContactBob"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ApplicationContact.objects.count(), 1)

    def test_add_application_renewal(self):
        a = ApplicationFactory()
        response = self.c.post(
            reverse("add-application-renewal", args=(a.id,)),
            {
                "end": "2040-10-10",
                "notes": "this is a new renewal",
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Lease.objects.count(), 1)
        self.assertTrue(a.valid_renewal())

    def test_renewals_dashboard(self):
        a = ApplicationFactory()
        b = ApplicationFactory()
        response = self.c.get(reverse('renewals-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            a in response.context['apps_without_renewals'])
        self.assertTrue(
            b in response.context['apps_without_renewals'])
        # create a renewal for one
        response = self.c.post(
            reverse("add-application-renewal", args=(b.id,)),
            {
                "end": "2040-10-10",
                "notes": "this is a new renewal",
            }
        )
        response = self.c.get(reverse('renewals-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            a in response.context['apps_without_renewals'])
        self.assertFalse(
            b in response.context['apps_without_renewals'])

    def test_add_server_form(self):
        response = self.c.get("/add_server/")
        self.assertEqual(response.status_code, 200)

    def test_add_application_form(self):
        response = self.c.get("/add_application/")
        self.assertEqual(response.status_code, 200)

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
        response = self.c.get(reverse('applications-view'))
        self.assertContains(response, 'testapp')

    def test_add_server(self):
        response = self.c.post(
            "/add_server/",
            {
                'location': 'test location',
                'name': 'testserver',
                'contact': 'Anders,Jonah',
                'ec2_instance_id': 'i-fde235eb',
            })
        self.assertEqual(response.status_code, 302)
        response = self.c.get(reverse('index-view'))
        self.assertContains(response, 'testserver')

        # pull up the server page
        s = Server.objects.get(name='testserver')
        response = self.c.get(s.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Anders')
        self.assertContains(response, 'i-fde235eb')

        loc = Location.objects.get(name="test location")
        response = self.c.get(loc.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testserver')

        # contacts should exist too
        c = Contact.objects.get(name="Anders")
        response = self.c.get(c.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Anders')
        self.assertContains(response, 'testserver')

    def test_add_server_alternates(self):
        response = self.c.post(
            "/add_server/",
            {
                'location': 'test location',
                'name': 'testserver',
                'contact': 'Anders,Jonah',
            })
        self.assertEqual(response.status_code, 302)
        response = self.c.get(reverse('index-view'))
        self.assertContains(response, 'testserver')

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
        self.assertEqual(response.status_code, 302)
        response = self.c.get("/server/%d/" % server.id)
        self.assertContains(response, 'test.example.com')

        a = Alias.objects.get(hostname='test.example.com')
        response = self.c.get("/alias/%d/" % a.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'admin info')

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

    def test_deprecated_application(self):
        application = ApplicationFactory(deprecated=True)
        response = self.c.get(reverse('index-view'))
        self.assertNotContains(response, application.get_absolute_url())

    def test_delete_servercontact(self):
        sc = ServerContactFactory()
        response = self.c.get(reverse('delete-servercontact', args=[sc.id]))
        self.assertEqual(response.status_code, 200)
        response = self.c.post(reverse('delete-servercontact', args=[sc.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ServerContact.objects.count(), 0)

    def test_delete_applicationcontact(self):
        ac = ApplicationContactFactory()
        response = self.c.get(reverse('delete-applicationcontact',
                                      args=[ac.id]))
        self.assertEqual(response.status_code, 200)
        response = self.c.post(reverse('delete-applicationcontact',
                                       args=[ac.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ApplicationContact.objects.count(), 0)

    def test_delete_alias(self):
        alias = AliasFactory()
        response = self.c.get("/alias/%d/delete/" % alias.id)
        self.assertEqual(response.status_code, 200)
        # should just be a confirmation
        self.assertEqual(Alias.objects.count(), 1)
        response = self.c.post("/alias/%d/delete/" % alias.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Alias.objects.count(), 0)

    def test_alias_confirm(self):
        alias = AliasFactory(status="pending")
        response = self.c.post("/alias/%d/confirm/" % alias.id)
        self.assertEqual(response.status_code, 302)
        response = self.c.get("/alias/%d/" % alias.id)
        self.assertNotContains(response, 'pending')

    def test_alias_edit_form(self):
        alias = AliasFactory(status="pending")
        response = self.c.get("/alias/%d/edit/" % alias.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        response = self.c.post(
            "/alias/%d/edit/" % alias.id,
            dict(hostname=alias.hostname,
                 status="active",
                 description="new description",
                 administrative_info="new admin info"),
        )
        self.assertEqual(response.status_code, 302)
        response = self.c.get("/alias/%d/" % alias.id)
        self.assertContains(response, 'new description')
        self.assertContains(response, 'new admin info')

    def test_alias_associate_with_application(self):
        alias = AliasFactory()
        application = ApplicationFactory()
        response = self.c.post(
            "/alias/%d/associate_with_application/" % alias.id,
            dict(application=application.id))
        self.assertEqual(response.status_code, 302)
