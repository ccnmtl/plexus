# Django settings for plexus project.
import os.path
from ccnmtlsettings.shared import common


project = 'plexus'
base = os.path.dirname(__file__)

locals().update(common(project=project, base=base))

PROJECT_APPS = ['plexus.main', 'plexus.grainlog']
USE_TZ = True

INSTALLED_APPS += [  # noqa
    'django_cas_ng',
    'bootstrapform',
    'bootstrap4',
    'plexus.main',
    'plexus.grainlog',
    'modelcluster',
    'taggit',
]

HOSTMASTER_EMAIL = "hostmaster@columbia.edu"
SYSADMIN_LIST_EMAIL = "ctl-sysadmin@columbia.edu"

MAX_GRAINLOGS = 10

INSTALLED_APPS.remove('djangowind')  # noqa

MIDDLEWARE += [  # noqa
    'django_cas_ng.middleware.CASMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend'
]

CAS_SERVER_URL = 'https://cas.columbia.edu/cas/'
CAS_VERSION = '3'
CAS_ADMIN_REDIRECT = False

# Translate CUIT's CAS user attributes to the Django user model.
# https://cuit.columbia.edu/content/cas-3-ticket-validation-response
CAS_APPLY_ATTRIBUTES_TO_USER = True
CAS_RENAME_ATTRIBUTES = {
    'givenName': 'first_name',
    'lastName': 'last_name',
    'mail': 'email',
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(base, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'stagingcontext.staging_processor',
                'gacontext.ga_processor'
            ],
        },
    },
]
