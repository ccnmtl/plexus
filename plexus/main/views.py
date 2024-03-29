from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView, DeleteView
from django.views.generic.base import View

from plexus.grainlog.grain import Grain
from plexus.grainlog.models import GrainLog
from plexus.main.models import (
    Server, Alias, Location, IPAddress,
    ServerNote, Note, Application, Technology,
    ApplicationAlias, ServerContact, ApplicationNote, ApplicationContact,
    Lease,
)


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class IndexView(LoggedInMixin, TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        ctx = TemplateView.get_context_data(self, **kwargs)

        ctx['servers'] = Server.objects.filter(
            deprecated=False).order_by('name').select_related('location')
        ctx['applications'] = Application.objects.filter(deprecated=False)
        ctx['logs'] = GrainLog.objects.all()

        grainlog = GrainLog.objects.current_grainlog()
        if grainlog:
            grain = Grain(grainlog.data())
            ctx['grains'] = grain.servers()
        return ctx


class AliasesView(LoggedInMixin, TemplateView):
    template_name = 'main/aliases.html'

    def get_context_data(self):
        return dict(
            aliases=(
                Alias.objects.all().exclude(status='deprecated').order_by(
                    'hostname'
                ).select_related('ip_address__server')),
        )


class ApplicationsView(LoggedInMixin, TemplateView):
    template_name = 'main/applications.html'

    def get_context_data(self):
        return dict(
            applications=Application.objects.filter(deprecated=False).order_by(
                'name').select_related('technology'),
        )


class AddServerView(LoggedInMixin, View):
    template_name = 'main/add_server.html'

    def post(self, request):
        location, created = Location.objects.get_or_create(
            name=request.POST.get("location", "unknown"))
        name = request.POST.get('name', 'unknown server')
        graphite_name = request.POST.get('graphite_name', '')
        server = Server.objects.create(
            name=name,
            primary_function=request.POST.get('primary_function', ''),
            location=location,
            notes=request.POST.get('notes', ''),
            graphite_name=graphite_name,
            ec2_instance_id=request.POST.get('ec2_instance_id', ''),
        )

        server.set_contacts(request.POST.get('contact', '').split(','))
        return HttpResponseRedirect(reverse('index-view'))

    def get(self, request):
        return render(
            request,
            self.template_name,
            dict(all_locations=Location.objects.all())
        )


class AddServerContactView(LoggedInMixin, View):
    def post(self, request, pk):
        server = get_object_or_404(Server, pk=pk)
        contact = request.POST.get('contact')
        server.add_contacts([contact])
        return HttpResponseRedirect(server.get_absolute_url())


class DeleteServerContactView(LoggedInMixin, DeleteView):
    model = ServerContact

    def get_success_url(self):
        return reverse('server-detail', args=[self.object.server.id])


class DeleteApplicationContactView(LoggedInMixin, DeleteView):
    model = ApplicationContact

    def get_success_url(self):
        return reverse('application-detail', args=[self.object.application.id])


class AddAliasView(LoggedInMixin, View):
    def post(self, request, id):
        server = get_object_or_404(Server, id=id)
        ipaddress_id = request.POST.get('ipaddress', None)
        ipaddress = server.ipaddress_default(ipaddress_id)
        Alias.objects.create(
            hostname=request.POST.get('hostname', '[none]'),
            ip_address=ipaddress,
            description=request.POST.get('description', ''),
            administrative_info=request.POST.get('administrative_info', ''),
        )
        return HttpResponseRedirect("/server/%d/" % server.id)


class RequestAliasView(LoggedInMixin, View):
    def post(self, request, id):
        server = get_object_or_404(Server, id=id)
        ipaddress_id = request.POST.get('ipaddress', None)
        ipaddress = server.ipaddress_default(ipaddress_id)
        alias = Alias.objects.create(
            hostname=request.POST.get('hostname', '[none]'),
            ip_address=ipaddress,
            description=request.POST.get('description', ''),
            status='pending',
        )
        subject = alias.dns_request_email_subject()
        body = alias.dns_request_email_body(request.user.first_name)
        send_mail(subject, body, settings.SERVER_EMAIL,
                  [settings.HOSTMASTER_EMAIL,
                   settings.SYSADMIN_LIST_EMAIL,
                   request.user.email])

        return HttpResponseRedirect("/server/%d/" % server.id)


class RequestAliasChangeView(LoggedInMixin, View):
    def post(self, request, id):
        alias = get_object_or_404(Alias, id=id)
        current_server = alias.ip_address.server
        current_ip_address = alias.ip_address

        new_ipaddress_id = request.POST.get('new_ipaddress', None)
        new_ip_address = get_object_or_404(IPAddress, id=new_ipaddress_id)

        alias.ip_address = new_ip_address
        alias.status = "pending"
        alias.save()

        subject = alias.dns_change_request_email_subject()
        body = alias.dns_change_request_email_body(
            current_server, current_ip_address,
            request.user.first_name)
        send_mail(subject, body, settings.SERVER_EMAIL,
                  [settings.HOSTMASTER_EMAIL,
                   settings.SYSADMIN_LIST_EMAIL,
                   request.user.email])

        return HttpResponseRedirect("/alias/%d/" % alias.id)


class AliasChangeView(LoggedInMixin, View):
    def post(self, request, id):
        alias = get_object_or_404(Alias, id=id)

        new_ipaddress_id = request.POST.get('new_ipaddress', None)
        new_ip_address = get_object_or_404(IPAddress, id=new_ipaddress_id)

        alias.ip_address = new_ip_address
        alias.save()

        return HttpResponseRedirect("/alias/%d/" % alias.id)


class AliasView(LoggedInMixin, DetailView):
    model = Alias

    def get_context_data(self, **kwargs):
        context = super(AliasView, self).get_context_data(**kwargs)
        context['all_applications'] = Application.objects.all()
        context['all_servers'] = Server.objects.filter(deprecated=False)
        return context


class AliasConfirmView(LoggedInMixin, View):
    def post(self, request, id):
        alias = get_object_or_404(Alias, id=id)
        alias.status = 'active'
        alias.save()
        return HttpResponseRedirect("/alias/%d/" % alias.id)


class AliasDeleteView(LoggedInMixin, DeleteView):
    model = Alias
    success_url = "/"


class AliasAssociateWithApplicationView(LoggedInMixin, View):
    def post(self, request, id):
        alias = get_object_or_404(Alias, id=id)
        application = get_object_or_404(
            Application,
            id=request.POST.get('application', '0'))
        ApplicationAlias.objects.create(alias=alias, application=application)
        return HttpResponseRedirect("/alias/%d/" % alias.id)


class AddApplicationView(LoggedInMixin, View):
    template_name = 'main/add_application.html'

    def post(self, request):
        technology, created = Technology.objects.get_or_create(
            name=request.POST.get("technology", "unknown"))
        name = request.POST.get('name', 'unknown application')
        graphite_name = request.POST.get('graphite_name', '')
        application = Application.objects.create(
            name=name,
            description=request.POST.get('description', ''),
            technology=technology,
            pmt_id=request.POST.get('pmt_id', '') or '0',
            graphite_name=graphite_name,
            sentry_name=request.POST.get('sentry_name', ''),
            repo=request.POST.get('repo', ''),
            github_url=request.POST.get('github_url', ''),
        )
        application.set_contacts(request.POST.get('contact', '').split(','))
        return HttpResponseRedirect(reverse('index-view'))

    def get(self, request):
        return render(
            request,
            self.template_name,
            dict(all_technologies=Technology.objects.all()))


class AddApplicationContactView(LoggedInMixin, View):
    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        contact = request.POST.get('contact')
        application.add_contacts([contact])
        return HttpResponseRedirect(application.get_absolute_url())


class AddServerNoteView(LoggedInMixin, View):
    def post(self, request, pk):
        server = get_object_or_404(Server, pk=pk)
        n = Note.objects.create(
            user=request.user, body=request.POST.get('body', ''))
        ServerNote.objects.create(
            server=server, note=n)
        return HttpResponseRedirect(server.get_absolute_url())


class AddApplicationNoteView(LoggedInMixin, View):
    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        n = Note.objects.create(
            user=request.user, body=request.POST.get('body', ''))
        ApplicationNote.objects.create(
            application=application, note=n)
        return HttpResponseRedirect(application.get_absolute_url())


class AddApplicationRenewal(LoggedInMixin, View):
    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        end = request.POST.get('end')
        notes = request.POST.get('notes')
        Lease.objects.create(application=application, end=end, notes=notes,
                             user=request.user)
        return HttpResponseRedirect(reverse('application-detail', args=[pk]))


class RenewalsDashboard(LoggedInMixin, TemplateView):
    template_name = "main/renewals_dashboard.html"

    def get_context_data(self, *args, **kwargs):
        now = datetime.now()
        active_renewals = Lease.objects.filter(
            end__gte=now,
        ).exclude(application__deprecated=True).order_by('end')
        active_applications = set([r.application for r in active_renewals])
        all_applications = set(a for a in Application.objects.filter(
            deprecated=False))
        apps_without_renewals = all_applications - active_applications
        return dict(
            active_renewals=active_renewals,
            apps_without_renewals=sorted(list(apps_without_renewals),
                                         key=lambda x: x.name.lower()),
        )


class ServerDetailView(LoggedInMixin, DetailView):
    model = Server
    template_name = "main/server_detail.html"

    def get_context_data(self, *args, **kwargs):
        ctx = DetailView.get_context_data(self, **kwargs)

        grainlog = GrainLog.objects.current_grainlog()
        if grainlog:
            ctx['grains'] = Grain(grainlog.data()).servers()

        return ctx
