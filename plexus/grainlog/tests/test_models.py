from django.conf import settings
from django.test import TestCase
from .factories import GrainLogFactory
from plexus.grainlog.models import GrainLog


class TestGrainLog(TestCase):
    def test_trivial(self):
        gl = GrainLogFactory()
        self.assertIsNotNone(gl)


class TestGrainLogManager(TestCase):
    def test_create_grainlog_simple(self):
        gl = GrainLog.objects.create_grainlog(sha1='foo', payload='bar')
        self.assertEqual(gl.sha1, 'foo')
        self.assertEqual(gl.payload, 'bar')

    def test_create_grainlog_no_duplicate(self):
        GrainLog.objects.create_grainlog(sha1='abcd')
        self.assertEqual(GrainLog.objects.all().count(), 1)
        GrainLog.objects.create_grainlog(sha1='abcd')
        self.assertEqual(GrainLog.objects.all().count(), 1)
        GrainLog.objects.create_grainlog(sha1='efgh')
        self.assertEqual(GrainLog.objects.all().count(), 2)

    def test_create_grainlog_no_limit_number(self):
        # all good up to the max
        for i in range(settings.MAX_GRAINLOGS):
            GrainLog.objects.create_grainlog(sha1=str(i))
            self.assertEqual(GrainLog.objects.all().count(), i + 1)
        # the first one inserted should still be there
        self.assertEqual(GrainLog.objects.filter(sha1='0').count(), 1)
        # but now it should clear out old ones
        max_sha1 = str(settings.MAX_GRAINLOGS + 1)
        GrainLog.objects.create_grainlog(sha1=max_sha1)
        self.assertEqual(GrainLog.objects.all().count(),
                         settings.MAX_GRAINLOGS)
        # our most recent should be in there
        self.assertEqual(GrainLog.objects.filter(sha1=max_sha1).count(), 1)
        # but the earliest should be gone now
        self.assertEqual(GrainLog.objects.filter(sha1='0').count(), 0)
