# Django settings for plexus project.
import os.path
from ccnmtlsettings.shared import common


project = 'plexus'
base = os.path.dirname(__file__)

locals().update(common(project=project, base=base))

PROJECT_APPS = ['plexus.main', 'plexus.grainlog']
USE_TZ = True

INSTALLED_APPS += [  # noqa
    'bootstrapform',
    'bootstrap3',
    'plexus.main',
    'plexus.grainlog',
    'modelcluster',
    'taggit',
]

HOSTMASTER_EMAIL = "hostmaster@columbia.edu"
SYSADMIN_LIST_EMAIL = "ctl-sysadmin@columbia.edu"

MAX_GRAINLOGS = 10
