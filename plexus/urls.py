from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from plexus.main.views import IndexView, ServerView, ContactView
import os.path
admin.autodiscover()
import staticmedia

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

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
    (r'^add_server/$', 'plexus.main.views.add_server'),
    (r'^server/(?P<pk>\d+)/$', ServerView.as_view()),
    (r'^server/(?P<id>\d+)/add_alias/$',
     'plexus.main.views.add_alias'),
    (r'^server/(?P<id>\d+)/request_alias/$',
     'plexus.main.views.request_alias'),
    (r'^server/(?P<id>\d+)/associate_dom0/$',
     'plexus.main.views.associate_dom0'),

    (r'^alias/(?P<id>\d+)/$',
     'plexus.main.views.alias'),
    (r'^alias/(?P<id>\d+)/confirm/$',
     'plexus.main.views.alias_confirm'),
    (r'^alias/(?P<id>\d+)/delete/$',
     'plexus.main.views.alias_delete'),
    (r'^alias/(?P<id>\d+)/associate_with_application/$',
     'plexus.main.views.alias_associate_with_application'),
    (r'^alias/(?P<id>\d+)/request_alias_change/$',
     'plexus.main.views.request_alias_change'),

    (r'^contact/(?P<pk>\d+)/$', ContactView.as_view()),
    (r'^contact/(?P<id>\d+)/dashboard/$',
     'plexus.main.views.contact_dashboard'),

    (r'^add_application/$',
     'plexus.main.views.add_application'),
    (r'^application/(?P<id>\d+)/$',
     'plexus.main.views.application'),

    (r'^os/(?P<id>\d+)/$',
     'plexus.main.views.os_family'),
    (r'^os/(?P<family_id>\d+)/(?P<id>\d+)/$',
     'plexus.main.views.os_version'),

    (r'^location/(?P<id>\d+)/$',
     'plexus.main.views.location'),

    (r'^render', 'plexus.main.views.render_proxy'),
    (r'^metrics', 'plexus.main.views.metrics_proxy'),

    (r'^inplaceeditform/', include('inplaceeditform.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^munin/', include('munin.urls')),
    url(r'^impersonate/', include('impersonate.urls')),
    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'^stats/auth/$', TemplateView.as_view(template_name="auth_stats.html")),
    (r'smoketest/', include('smoketest.urls')),
    (r'^site_media/(?P<path>.*)$',
     'django.views.static.serve',
     {'document_root': site_media_root}),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
) + staticmedia.serve()
