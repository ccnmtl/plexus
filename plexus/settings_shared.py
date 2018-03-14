# Django settings for plexus project.
import djcelery
import os.path
from ccnmtlsettings.shared import common
from django_feedparser.settings import *  # noqa
import urllib3.contrib.pyopenssl

# Tell urllib3 to use pyOpenSSL. Needed by python < 2.7.9
# to resolve an SNIMissingWarning.
# See:
#   https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl-py2
#   https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
urllib3.contrib.pyopenssl.inject_into_urllib3()

project = 'plexus'
base = os.path.dirname(__file__)

locals().update(common(project=project, base=base))

PROJECT_APPS = ['plexus.main', 'plexus.grainlog']
USE_TZ = True

djcelery.setup_loader()

INSTALLED_APPS += [  # noqa
    'bootstrapform',
    'bootstrap3',
    'django_feedparser',
    'plexus.main',
    'plexus.grainlog',
    'modelcluster',
    'taggit',
    'djcelery',
]

HOSTMASTER_EMAIL = "hostmaster@columbia.edu"
SYSADMIN_LIST_EMAIL = "ccnmtl-sysadmin@columbia.edu"

MAX_GRAINLOGS = 10

BROKER_URL = "amqp://localhost:5672//" + project

CELERYD_CONCURRENCY = 2
