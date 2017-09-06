# flake8: noqa
from plexus.settings_shared import *

try:
    from local_settings import *
except ImportError:
    pass
