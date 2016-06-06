import json

from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from plexus.grainlog.views import (
    GrainLogListView, GrainLogDetailView, RawView)
from .factories import GrainLogFactory


class ViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.anon = AnonymousUser()


class GrainLogListViewTest(ViewTest):
    def test_get(self):
        gl = GrainLogFactory()
        request = self.factory.get(reverse('grainlog-list'))
        request.user = self.anon
        response = GrainLogListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(gl in response.context_data['object_list'])
        self.assertTrue(reverse('grainlog-detail', args=[gl.id])
                        in response.rendered_content)

    def test_post(self):
        request = self.factory.post(reverse('grainlog-list'))
        with open('test_data/grains.json') as f:
            request.FILES['payload'] = SimpleUploadedFile("grains.json",
                                                          f.read())
            request.user = self.anon
            response = GrainLogListView.as_view()(request)
            self.assertEqual(response.status_code, 302)


class GrainLogDetailViewTest(ViewTest):
    def test_get(self):
        gl = GrainLogFactory()
        request = self.factory.get(reverse('grainlog-detail', args=[gl.id]))
        request.user = self.anon
        response = GrainLogDetailView.as_view()(request, pk=gl.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data['object'] == gl)
        self.assertTrue(gl.sha1 in response.rendered_content)


class RawViewTest(ViewTest):
    def test_get(self):
        gl = GrainLogFactory()
        request = self.factory.get(reverse('grainlog-raw'))
        response = RawView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        d = json.loads(response.content)
        self.assertEqual(gl.data(), d)

    def test_none(self):
        request = self.factory.get(reverse('grainlog-raw'))
        response = RawView.as_view()(request)
        self.assertEqual(response.status_code, 404)
