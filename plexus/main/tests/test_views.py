from django.test import TestCase
from django.test.client import Client
from plexus.main.models import Server
from plexus.main.models import Contact
from plexus.main.models import OSFamily
from plexus.main.models import OperatingSystem
from plexus.main.models import Location


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
