from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel


class EntryIndex(Page):
    @property
    def entries(self):
        entries = Entry.objects.live().descendant_of(self)
        # sort here if desired
        return entries


class Entry(Page):

    partner = models.CharField(max_length=256, blank=True)
    group = models.CharField(max_length=256, blank=True)
    site_url = models.URLField()
    thumb_url = models.URLField()
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

    @property
    def entry_index(self):
        return self.get_ancestors().type(EntryIndex).last()

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        FieldPanel('partner'),
        FieldPanel('group'),
        FieldPanel('site_url'),
        FieldPanel('thumb_url'),
        FieldPanel('access'),
        FieldPanel('status'),
        FieldPanel('orig_release'),
        FieldPanel('info_url'),
        FieldPanel('info_descriptor'),
    ]
