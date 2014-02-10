# flake8: noqa
from settings_shared import *
import sys

TEMPLATE_DIRS = (
    "/var/www/plexus/plexus/plexus/templates",
)

MEDIA_ROOT = '/var/www/plexus/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/plexus/plexus/sitemedia'),
)

COMPRESS_ROOT = "/var/www/plexus/plexus/media/"
DEBUG = False
TEMPLATE_DEBUG = DEBUG

SENTRY_SITE = 'plexus'
SENTRY_SERVERS = ['http://sentry.ccnmtl.columbia.edu/sentry/store/']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'plexus',
        'HOST': '',
        'PORT': 6432,
        'USER': '',
        'PASSWORD': '',
        }
}

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

try:
    from local_settings import *
except ImportError:
    pass
