# flake8: noqa
from plexus.settings_shared import *
from ctlsettings.docker import common
import os

BROKER_URL = os.environ['BROKER_URL']

locals().update(
    common(
        project=project,
        base=base,
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
    ))
