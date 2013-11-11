from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView, DetailView, UpdateView
from plexus.main.models import Location, OperatingSystem, Server
from plexus.main.models import OSFamily, Application, Contact
from plexus.main.models import Alias
from plexus.main.forms import AliasForm, ContactForm, ServerForm
from plexus.main.forms import ApplicationForm
from plexus.main.views import IndexView
from plexus.main.views import AliasDeleteView, AddServerView
from plexus.main.views import AssociateDom0View, AddAliasView
from plexus.main.views import RequestAliasView, AddApplicationView
from plexus.main.views import AliasView, RequestAliasChangeView
from plexus.main.views import AliasConfirmView
from plexus.main.views import AliasAssociateWithApplicationView
from plexus.main.views import GraphiteProxyView
import os.path
admin.autodiscover()

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))
logout_page = (r'^accounts/logout/$', 'django.contrib.auth.views.logout',
               {'next_page': redirect_after_logout})
if hasattr(settings, 'WIND_BASE'):
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
    (r'^server/(?P<pk>\d+)/$', DetailView.as_view(model=Server)),
    (r'^server/(?P<pk>\d+)/edit/$',
     UpdateView.as_view(model=Server,
                        form_class=ServerForm)),
    (r'^server/(?P<id>\d+)/add_alias/$', AddAliasView.as_view()),
    (r'^server/(?P<id>\d+)/request_alias/$', RequestAliasView.as_view()),
    (r'^server/(?P<id>\d+)/associate_dom0/$', AssociateDom0View.as_view()),

    (r'^alias/(?P<pk>\d+)/$', AliasView.as_view()),
    (r'^alias/(?P<id>\d+)/confirm/$', AliasConfirmView.as_view()),
    (r'^alias/(?P<pk>\d+)/delete/$', AliasDeleteView.as_view()),
    (r'^alias/(?P<pk>\d+)/edit/$',
     UpdateView.as_view(model=Alias,
                        form_class=AliasForm)),
    (r'^alias/(?P<id>\d+)/associate_with_application/$',
     AliasAssociateWithApplicationView.as_view()),
    (r'^alias/(?P<id>\d+)/request_alias_change/$',
     RequestAliasChangeView.as_view()),

    (r'^contact/(?P<pk>\d+)/$', DetailView.as_view(model=Contact)),
    (r'^contact/(?P<pk>\d+)/dashboard/$',
     DetailView.as_view(model=Contact,
                        template_name="main/contact_dashboard.html")),
    (r'^contact/(?P<pk>\d+)/edit/$',
     UpdateView.as_view(model=Contact,
                        form_class=ContactForm)),

    (r'^add_application/$', AddApplicationView.as_view()),
    (r'^application/(?P<pk>\d+)/$', DetailView.as_view(model=Application)),
    (r'^application/(?P<pk>\d+)/edit/$',
     UpdateView.as_view(model=Application, form_class=ApplicationForm)),

    (r'^os/(?P<pk>\d+)/$', DetailView.as_view(model=OSFamily)),
    (r'^os/(?P<family_id>\d+)/(?P<pk>\d+)/$',
     DetailView.as_view(model=OperatingSystem)),

    (r'^location/(?P<pk>\d+)/$', DetailView.as_view(model=Location)),

    (r'^render', GraphiteProxyView.as_view()),
    (r'^metrics', GraphiteProxyView.as_view()),

    (r'^inplaceeditform/', include('inplaceeditform.urls')),
    (r'^admin/', include(admin.site.urls)),
    url(r'^impersonate/', include('impersonate.urls')),
    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'^stats/auth/$', TemplateView.as_view(template_name="auth_stats.html")),
    (r'smoketest/', include('smoketest.urls')),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
)
