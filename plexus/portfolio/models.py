from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel


class Entry(Page):

    partner = models.CharField(max_length=256)
    group = models.CharField(max_length=256)
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
    orig_release = models.CharField(max_length=256)
    info_url = models.URLField()
    info_descriptor = models.CharField(max_length=256)

    body = RichTextField(blank=True)

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
