import hashlib

from django.core.urlresolvers import reverse
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from plexus.grainlog.models import GrainLog


class GrainLogListView(ListView):
    model = GrainLog

    def post(self, request, **kwargs):
        f = request.FILES.get('payload', None)
        if f is None:
            return HttpResponseBadRequest()

        # typical grainlog uploads are around 200k, which
        # is small enough that I think we can get away
        # with just turning it into a string in memory
        payload = ''.join(list(f.chunks()))

        sha1 = hashlib.sha1(payload).hexdigest()
        gl = self.model.objects.create_grainlog(sha1=sha1, payload=payload)
        return HttpResponseRedirect(reverse('grainlog-detail', args=[gl.id]))


class GrainLogDetailView(DetailView):
    model = GrainLog
