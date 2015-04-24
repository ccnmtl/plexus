# flake8: noqa
from settings_shared import *
import sys
import os

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

AWS_S3_CUSTOM_DOMAIN = "d35pxobnzf6ttf.cloudfront.net"
AWS_STORAGE_BUCKET_NAME = "ccnmtl-plexus-static-prod"
AWS_PRELOAD_METADATA = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'plexus.s3utils.MediaRootS3BotoStorage'
S3_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN
STATIC_URL = 'https://%s/media/' % AWS_S3_CUSTOM_DOMAIN
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL

DEFAULT_FILE_STORAGE = 'plexus.s3utils.MediaRootS3BotoStorage'
MEDIA_URL = S3_URL + 'media/'
COMPRESS_STORAGE = 'plexus.s3utils.CompressorS3BotoStorage'

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

try:
    from local_settings import *
except ImportError:
    pass
