# Django settings for plexus project.
import djcelery
import os.path
from ccnmtlsettings.shared import common
from django_feedparser.settings import *  # noqa

project = 'plexus'
base = os.path.dirname(__file__)

locals().update(common(project=project, base=base))

PROJECT_APPS = ['plexus.main', 'plexus.grainlog']
USE_TZ = True

MIDDLEWARE_CLASSES += [  # noqa
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
]

djcelery.setup_loader()

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

    'plexus.portfolio',

    'djcelery',
]

HOSTMASTER_EMAIL = "hostmaster@columbia.edu"
SYSADMIN_LIST_EMAIL = "ccnmtl-sysadmin@columbia.edu"

MAX_GRAINLOGS = 10

WAGTAIL_SITE_NAME = 'Plexus'

BROKER_URL = "amqp://localhost:5672//" + project

CELERYD_CONCURRENCY = 2
