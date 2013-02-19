from django.test import TestCase
from plexus.main.models import Location


class BasicTest(TestCase):
    def setUp(self):
        self.l = Location.objects.create(
            name="test",
            details="test location")

    def tearDown(self):
        self.l.delete()

    def test_retrieve(self):
        self.assertEquals(str(self.l), "test")
