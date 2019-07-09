# flake8: noqa
from plexus.settings_shared import *
from ccnmtlsettings.staging import common
import os

project = 'plexus'
base = os.path.dirname(__file__)

locals().update(
    common(
        project=project,
        base=base,
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
        cloudfront="d1vy4q2u1y7bpg",
    ))

try:
    from plexus.local_settings import *
except ImportError:
    pass
