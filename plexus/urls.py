from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import (
    TemplateView, DetailView, UpdateView, ListView)
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls
from plexus.main.models import Location, OperatingSystem, Server
from plexus.main.models import OSFamily, Application, Contact
from plexus.main.models import Alias
from plexus.main.forms import AliasForm, ContactForm, ServerForm
from plexus.main.forms import ApplicationForm
from plexus.main.views import (
    IndexView, AliasDeleteView, AddServerView,
    AddAliasView, RequestAliasView, AddApplicationView, AliasView,
    RequestAliasChangeView, AliasChangeView, AliasConfirmView,
    AliasAssociateWithApplicationView,
    AddServerNoteView, AddApplicationNoteView,
    DeleteServerContactView, DeleteApplicationContactView,
    AddApplicationContactView, AddServerContactView,
)

admin.autodiscover()

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))
logout_page = (r'^accounts/logout/$', 'django.contrib.auth.views.logout',
               {'next_page': redirect_after_logout})
if hasattr(settings, 'CAS_BASE') or hasattr(settings, 'WIND_BASE'):
    auth_urls = (r'^accounts/', include('djangowind.urls'))
    logout_page = (r'^accounts/logout/$',
                   'djangowind.views.logout',
                   {'next_page': redirect_after_logout})

urlpatterns = patterns(
    '',
    # Example:
    auth_urls,
    logout_page,
    (r'^$', IndexView.as_view()),
    (r'^add_server/$', AddServerView.as_view()),
    url(r'^server/(?P<pk>\d+)/$', DetailView.as_view(model=Server),
        name="server-detail"),
    (r'^server/(?P<pk>\d+)/edit/$',
     UpdateView.as_view(model=Server,
                        form_class=ServerForm)),
    url(r'server/(?P<pk>\d+)/add_contact/$', AddServerContactView.as_view(),
        name='add-server-contact'),
    (r'^server/(?P<id>\d+)/add_alias/$', AddAliasView.as_view()),
    url(r'^server/(?P<pk>\d+)/add_note/$', AddServerNoteView.as_view(),
        name="add-server-note"),
    (r'^server/(?P<id>\d+)/request_alias/$', RequestAliasView.as_view()),

    url(r'^servercontact/(?P<pk>\d+)/delete/$',
        DeleteServerContactView.as_view(),
        name="delete-servercontact"),

    (r'^alias/(?P<pk>\d+)/$', AliasView.as_view()),
    (r'^alias/(?P<id>\d+)/confirm/$', AliasConfirmView.as_view()),
    url(r'^alias/(?P<pk>\d+)/delete/$', AliasDeleteView.as_view(),
        name='delete-alias'),
    (r'^alias/(?P<pk>\d+)/edit/$',
     UpdateView.as_view(model=Alias,
                        form_class=AliasForm)),
    (r'^alias/(?P<id>\d+)/associate_with_application/$',
     AliasAssociateWithApplicationView.as_view()),
    (r'^alias/(?P<id>\d+)/request_alias_change/$',
     RequestAliasChangeView.as_view()),
    url(r'^alias/(?P<id>\d+)/change/$', AliasChangeView.as_view(),
        name='alias-change'),

    (r'^contact/(?P<pk>\d+)/$', DetailView.as_view(model=Contact)),
    (r'^contact/(?P<pk>\d+)/dashboard/$',
     DetailView.as_view(model=Contact,
                        template_name="main/contact_dashboard.html")),
    (r'^contact/(?P<pk>\d+)/edit/$',
     UpdateView.as_view(model=Contact,
                        form_class=ContactForm)),

    (r'^add_application/$', AddApplicationView.as_view()),
    url(r'^application/(?P<pk>\d+)/$', DetailView.as_view(model=Application),
        name="application-detail"),
    (r'^application/(?P<pk>\d+)/edit/$',
     UpdateView.as_view(model=Application, form_class=ApplicationForm)),
    url(r'^application/(?P<pk>\d+)/add_note/$',
        AddApplicationNoteView.as_view(),
        name="add-application-note"),
    url(r'^application/(?P<pk>\d+)/add_contact/$',
        AddApplicationContactView.as_view(),
        name="add-application-contact"),

    url(r'^applicationcontact/(?P<pk>\d+)/delete/$',
        DeleteApplicationContactView.as_view(),
        name="delete-applicationcontact"),

    (r'^os/(?P<pk>\d+)/$', DetailView.as_view(model=OSFamily)),
    (r'^os/(?P<family_id>\d+)/(?P<pk>\d+)/$',
     DetailView.as_view(model=OperatingSystem)),

    (r'^location/(?P<pk>\d+)/$', DetailView.as_view(model=Location)),

    url(r'^dashboard/$', TemplateView.as_view(
        template_name="dashboard/index.html"),
        name="dashboard-index"),
    url(r'^dashboard/500s/$', ListView.as_view(
        model=Application,
        template_name='dashboard/500s.html'),
        name='500s-dashboard'),
    url(r'^dashboard/404s/$', ListView.as_view(
        model=Application,
        template_name='dashboard/404s.html'),
        name='404s-dashboard'),
    url(r'^dashboard/traffic/$', ListView.as_view(
        model=Application,
        template_name='dashboard/traffic.html'),
        name='traffic-dashboard'),
    url(r'^dashboard/response_times/$', ListView.as_view(
        model=Application,
        template_name='dashboard/response_time.html'),
        name='response-time-dashboard'),
    url(r'^dashboard/load/$', ListView.as_view(
        queryset=Server.objects.filter(deprecated=False),
        template_name='dashboard/load.html'),
        name='load-dashboard'),
    url(r'^dashboard/disk/$', ListView.as_view(
        queryset=Server.objects.filter(deprecated=False),
        template_name='dashboard/disk.html'),
        name='disk-dashboard'),
    url(r'^dashboard/network/$', ListView.as_view(
        queryset=Server.objects.filter(deprecated=False),
        template_name='dashboard/network.html'),
        name='network-dashboard'),

    (r'^admin/', include(admin.site.urls)),
    url(r'^impersonate/', include('impersonate.urls')),
    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'^stats/auth/$', TemplateView.as_view(template_name="auth_stats.html")),
    (r'smoketest/', include('smoketest.urls')),
    (r'grainlogs/', include('plexus.grainlog.urls')),

    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^pages/', include(wagtail_urls)),

    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
)
