from django.conf.urls import url

from .views import GrainLogListView, GrainLogDetailView, RawView

urlpatterns = [
    url(r'^$', GrainLogListView.as_view(), name='grainlog-list'),
    url(r'^raw/$', RawView.as_view(), name='grainlog-raw'),
    url(r'^(?P<pk>\d+)/$', GrainLogDetailView.as_view(),
        name='grainlog-detail'),
]
