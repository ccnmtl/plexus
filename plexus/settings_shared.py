# Django settings for plexus project.
import os.path
from ccnmtlsettings.shared import common
from django_feedparser.settings import *  # noqa

project = 'plexus'
base = os.path.dirname(__file__)

locals().update(common(project=project, base=base))

PROJECT_APPS = ['plexus.main', 'plexus.grainlog']
USE_TZ = True

TEMPLATE_CONTEXT_PROCESSORS += [  # noqa
    'django.contrib.messages.context_processors.messages',
]

INSTALLED_APPS += [  # noqa
    'bootstrapform',
    'bootstrap3',
    'django_feedparser',
    'plexus.main',
    'plexus.grainlog',

    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',
    'modelcluster',
    'taggit',
]

HOSTMASTER_EMAIL = "hostmaster@columbia.edu"
SYSADMIN_LIST_EMAIL = "ccnmtl-sysadmin@columbia.edu"

MAX_GRAINLOGS = 10
