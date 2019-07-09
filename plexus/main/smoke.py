from smoketest import SmokeTest
from plexus.main.models import Server


class DBConnectivity(SmokeTest):
    def test_retrieve(self):
        cnt = Server.objects.all().count()
        self.assertTrue(cnt > 0)
