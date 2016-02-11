from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from plexus.grainlog.views import GrainLogListView, GrainLogDetailView
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
        self.assertTrue(gl.sha1 in response.rendered_content)


class GrainLogDetailViewTest(ViewTest):
    def test_get(self):
        gl = GrainLogFactory()
        request = self.factory.get(reverse('grainlog-detail', args=[gl.id]))
        request.user = self.anon
        response = GrainLogDetailView.as_view()(request, pk=gl.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data['object'] == gl)
        self.assertTrue(gl.sha1 in response.rendered_content)
