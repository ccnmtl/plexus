from django.urls import path, re_path

from plexus.grainlog.views import (
    GrainLogListView, GrainLogDetailView, RawView, RawUpdateView)


urlpatterns = [
    path('', RawUpdateView.as_view(), name='grainlog-raw-update'),
    path('list/', GrainLogListView.as_view(), name='grainlog-list'),
    path('raw/', RawView.as_view(), name='grainlog-raw'),
    re_path(r'^(?P<pk>\d+)/$', GrainLogDetailView.as_view(),
            name='grainlog-detail'),
]
