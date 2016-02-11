from django.views.generic import ListView, DetailView
from plexus.grainlog.models import GrainLog


class GrainLogListView(ListView):
    model = GrainLog


class GrainLogDetailView(DetailView):
    model = GrainLog
