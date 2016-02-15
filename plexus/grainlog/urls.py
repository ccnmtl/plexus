from django.conf.urls import url

from .views import GrainLogListView, GrainLogDetailView

urlpatterns = [
    url(r'^$', GrainLogListView.as_view(), name='grainlog-list'),
    url(r'^(?P<pk>\d+)/$', GrainLogDetailView.as_view(),
        name='grainlog-detail'),
]
