# flake8: noqa
from settings_shared import *
from ccnmtlsettings.compose import common

locals().update(
    common(
        project=project,
        base=base,
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
    ))

BROKER_URL = "amqp://guest:guest@rabbitmq:5672/"

try:
    from local_settings import *
except ImportError:
    pass

print(BROKER_URL)
