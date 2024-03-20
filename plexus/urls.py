from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
import django.contrib.auth.views
from django.urls import include, path
from django.views.generic import (
    TemplateView, DetailView, UpdateView, ListView)
import django.views.static
from django_cas_ng import views as cas_views
from plexus.main.forms import AliasForm, ContactForm, ServerForm
from plexus.main.forms import ApplicationForm
from plexus.main.models import Alias
from plexus.main.models import Location, Server
from plexus.main.models import Application, Contact
from plexus.main.views import (
    IndexView, AliasDeleteView, AddServerView,
    AddAliasView, RequestAliasView, AddApplicationView, AliasView,
    RequestAliasChangeView, AliasChangeView, AliasConfirmView,
    AliasAssociateWithApplicationView,
    AddServerNoteView, AddApplicationNoteView,
    DeleteServerContactView, DeleteApplicationContactView,
    AddApplicationContactView, AddServerContactView,
    AddApplicationRenewal, RenewalsDashboard,
    AliasesView, ApplicationsView, ServerDetailView
)


admin.autodiscover()

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('cas/login', cas_views.LoginView.as_view(),
         name='cas_ng_login'),
    path('cas/logout', cas_views.LogoutView.as_view(),
         name='cas_ng_logout'),

    path('', IndexView.as_view(), name="index-view"),
    path('aliases/', AliasesView.as_view(), name="aliases-view"),
    path('applications/', ApplicationsView.as_view(),
         name="applications-view"),
    path('add_server/', AddServerView.as_view()),
    path('server/<int:pk>/',
         ServerDetailView.as_view(),
         name="server-detail"),
    path('server/<int:pk>/edit/',
         login_required(
             UpdateView.as_view(model=Server, form_class=ServerForm))),
    path(r'server/<int:pk>/add_contact/', AddServerContactView.as_view(),
         name='add-server-contact'),
    path('server/<int:id>/add_alias/', AddAliasView.as_view()),
    path('server/<int:pk>/add_note/', AddServerNoteView.as_view(),
         name="add-server-note"),
    path('server/<int:id>/request_alias/', RequestAliasView.as_view()),

    path('servercontact/<int:pk>/delete/',
         DeleteServerContactView.as_view(),
         name="delete-servercontact"),

    path('alias/<int:pk>/', AliasView.as_view()),
    path('alias/<int:id>/confirm/', AliasConfirmView.as_view()),
    path('alias/<int:pk>/delete/', AliasDeleteView.as_view(),
         name='delete-alias'),
    path('alias/<int:pk>/edit/', login_required(UpdateView.as_view(
        model=Alias, form_class=AliasForm))),
    path('alias/<int:id>/associate_with_application/',
         AliasAssociateWithApplicationView.as_view()),
    path('alias/<int:id>/request_alias_change/',
         RequestAliasChangeView.as_view()),
    path('alias/<int:id>/change/', AliasChangeView.as_view(),
         name='alias-change'),

    path('contact/<int:pk>/',
         login_required(DetailView.as_view(model=Contact))),
    path('contact/<int:pk>/dashboard/',
         login_required(DetailView.as_view(
             model=Contact, template_name="main/contact_dashboard.html"))),
    path('contact/<int:pk>/edit/', login_required(UpdateView.as_view(
        model=Contact, form_class=ContactForm))),

    path('add_application/', AddApplicationView.as_view()),
    path('application/<int:pk>/',
         login_required(DetailView.as_view(model=Application)),
         name="application-detail"),
    path('application/<int:pk>/edit/',
         login_required(UpdateView.as_view(
             model=Application, form_class=ApplicationForm))),
    path('application/<int:pk>/add_note/',
         AddApplicationNoteView.as_view(), name="add-application-note"),
    path('application/<int:pk>/add_contact/',
         AddApplicationContactView.as_view(),
         name="add-application-contact"),
    path('application/<int:pk>/add_renewal/',
         AddApplicationRenewal.as_view(), name="add-application-renewal"),

    path('applicationcontact/<int:pk>/delete/',
         DeleteApplicationContactView.as_view(),
         name="delete-applicationcontact"),

    path(r'renewals/', RenewalsDashboard.as_view(),
         name='renewals-dashboard'),

    path('location/<int:pk>/', login_required(
        DetailView.as_view(model=Location))),

    path('dashboard/', login_required(TemplateView.as_view(
        template_name="dashboard/index.html")), name="dashboard-index"),
    path('dashboard/500s/', login_required(ListView.as_view(
        model=Application, template_name='dashboard/500s.html')),
         name='500s-dashboard'),
    path('dashboard/404s/', login_required(ListView.as_view(
        model=Application, template_name='dashboard/404s.html')),
         name='404s-dashboard'),
    path('dashboard/traffic/', login_required(ListView.as_view(
        model=Application, template_name='dashboard/traffic.html')),
         name='traffic-dashboard'),
    path('dashboard/response_times/', login_required(ListView.as_view(
        model=Application, template_name='dashboard/response_time.html')),
         name='response-time-dashboard'),
    path('dashboard/load/', login_required(ListView.as_view(
        queryset=Server.objects.filter(deprecated=False),
        template_name='dashboard/load.html')), name='load-dashboard'),
    path('dashboard/disk/', login_required(ListView.as_view(
        queryset=Server.objects.filter(deprecated=False),
        template_name='dashboard/disk.html')), name='disk-dashboard'),
    path('dashboard/network/', login_required(ListView.as_view(
        queryset=Server.objects.filter(deprecated=False),
        template_name='dashboard/network.html')), name='network-dashboard'),

    path('admin/', admin.site.urls),
    path('impersonate/', include('impersonate.urls')),
    path('stats/', TemplateView.as_view(template_name="stats.html")),
    path('stats/auth/', TemplateView.as_view(
        template_name="auth_stats.html")),
    path(r'smoketest/', include('smoketest.urls')),
    path(r'grainlogs/', include('plexus.grainlog.urls')),

    path('uploads/<slug:path>', django.views.static.serve,
         {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
