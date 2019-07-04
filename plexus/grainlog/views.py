import hashlib

from django.core.urlresolvers import reverse
from django.http.response import (
    HttpResponseBadRequest, HttpResponseRedirect, JsonResponse,
    HttpResponseNotFound,
)
from django.views.generic import ListView, DetailView, View
from django.utils.encoding import smart_text

from plexus.grainlog.models import GrainLog
from plexus.main.views import LoggedInMixin


class GrainLogListView(LoggedInMixin, ListView):
    model = GrainLog


class GrainLogDetailView(LoggedInMixin, DetailView):
    model = GrainLog


class RawView(View):
    def get(self, request):
        g = GrainLog.objects.current_grainlog()
        if g is None:
            return HttpResponseNotFound()
        return JsonResponse(g.data())


class RawUpdateView(View):
    model = GrainLog

    def post(self, request, **kwargs):
        f = request.FILES.get('payload', None)
        if f is None:
            return HttpResponseBadRequest()

        # typical grainlog uploads are around 200k, which
        # is small enough that I think we can get away
        # with just turning it into a string in memory
        payload = smart_text(f.read())
        encoded_payload = payload.encode('utf-8')

        sha1 = hashlib.sha1(encoded_payload).hexdigest()  # nosec
        gl = self.model.objects.create_grainlog(sha1=sha1, payload=encoded_payload)
        return HttpResponseRedirect(reverse('grainlog-detail', args=[gl.id]))
