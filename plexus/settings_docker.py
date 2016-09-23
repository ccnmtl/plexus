# flake8: noqa
from settings_shared import *
from ccnmtlsettings.docker import common
import os

project = 'plexus'
base = os.path.dirname(__file__)

locals().update(
    common(
        project=project,
        base=base,
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
    ))
