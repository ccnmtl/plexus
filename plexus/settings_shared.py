# Django settings for plexus project.
import os.path
from ccnmtlsettings.shared import common

project = 'plexus'
base = os.path.dirname(__file__)

locals().update(common(project=project, base=base))

PROJECT_APPS = ['plexus.main', ]
USE_TZ = True

TEMPLATE_CONTEXT_PROCESSORS += [  # noqa
    'django.contrib.messages.context_processors.messages',
]

INSTALLED_APPS += [  # noqa
    'django.contrib.messages',
    'bootstrapform',
    'bootstrap3',
    'template_utils',
    'plexus.main',
]

HOSTMASTER_EMAIL = "hostmaster@columbia.edu"
SYSADMIN_LIST_EMAIL = "ccnmtl-sysadmin@columbia.edu"
