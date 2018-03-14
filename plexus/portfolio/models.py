from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index


class EntryIndex(Page):
    subpage_types = ['portfolio.Entry']

    @property
    def entries(self):
        entries = Entry.objects.live().descendant_of(self)
        # sort here if desired
        return entries


class Entry(Page):

    partner = models.CharField(max_length=256, blank=True)
    group = models.CharField(max_length=256, blank=True)
    site_url = models.URLField()
    thumb = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    access = models.CharField(
        max_length=256,
        choices=[("Public", "Public"),
                 ("Protected", "Protected"),
                 ("Private", "Private")])
    status = models.CharField(
        max_length=256,
        choices=[("Development", "Development"),
                 ("Active", "Active"),
                 ("Archived", "Archived")])
    orig_release = models.CharField(max_length=256, blank=True)
    info_url = models.URLField(blank=True)
    info_descriptor = models.CharField(max_length=256, blank=True)

    body = RichTextField(blank=True)

    parent_page_types = ['portfolio.EntryIndex']
    subpage_types = []

    @property
    def entry_index(self):
        return self.get_ancestors().type(EntryIndex).last()

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        FieldPanel('partner'),
        FieldPanel('group'),
        FieldPanel('site_url'),
        ImageChooserPanel('thumb'),
        FieldPanel('access'),
        FieldPanel('status'),
        FieldPanel('orig_release'),
        FieldPanel('info_url'),
        FieldPanel('info_descriptor'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),

        index.FilterField('partner'),
        index.FilterField('group'),
        index.FilterField('access'),
        index.FilterField('status'),
    ]
