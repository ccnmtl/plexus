import os
from django.conf import settings
from plexus.settings_shared import *  # noqa: F403
from ctlsettings.production import common
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

project = 'plexus'
base = os.path.dirname(__file__)

locals().update(
    common(
        project=project,
        base=base,
        s3prefix="ccnmtl",
        STATIC_ROOT=STATIC_ROOT,  # noqa: F405
        INSTALLED_APPS=INSTALLED_APPS,  # noqa: F405
        cloudfront="d35pxobnzf6ttf",
    ))

try:
    from plexus.local_settings import *  # noqa: F403
except ImportError:
    pass

if hasattr(settings, 'SENTRY_DSN'):
    sentry_sdk.init(
        dsn=SENTRY_DSN,  # noqa: F405
        integrations=[DjangoIntegration()],
    )
