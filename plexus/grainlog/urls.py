from django.conf.urls import url

from plexus.grainlog.views import (
    GrainLogListView, GrainLogDetailView, RawView, RawUpdateView)


urlpatterns = [
    url(r'^$', RawUpdateView.as_view(), name='grainlog-raw-update'),
    url(r'^list/$', GrainLogListView.as_view(), name='grainlog-list'),
    url(r'^raw/$', RawView.as_view(), name='grainlog-raw'),
    url(r'^(?P<pk>\d+)/$', GrainLogDetailView.as_view(),
        name='grainlog-detail'),
]
