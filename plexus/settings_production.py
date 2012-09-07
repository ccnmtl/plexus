from settings_shared import *

TEMPLATE_DIRS = (
    "/var/www/plexus/plexus/templates",
)

MEDIA_ROOT = '/var/www/plexus/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/plexus/plexus/sitemedia'),
)

COMPRESS_ROOT = "/var/www/plexus/plexus/media/"
DEBUG = False
TEMPLATE_DEBUG = DEBUG

try:
    from local_settings import *
except ImportError:
    pass
