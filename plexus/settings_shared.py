# Django settings for plexus project.
import os.path
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

ALLOWED_HOSTS = ['.ccnmtl.columbia.edu', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'plexus',
        'HOST': '',
        'PORT': 5432,
        'USER': '',
        'PASSWORD': '',
    }
}

if 'test' in sys.argv or 'jenkins' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
        }
    }

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=plexus',
]

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
)

PROJECT_APPS = ['plexus.main', ]
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

SOUTH_TESTS_MIGRATE = False


USE_TZ = True
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = "/var/www/plexus/uploads/"
MEDIA_URL = '/uploads/'
STATIC_URL = '/media/'
SECRET_KEY = ')ng#)ef_u@_^zvvu@dxm7ql-yb^_!a6%v3v^j3b(mp+)l+5%@h'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'stagingcontext.staging_processor',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
)

MIDDLEWARE_CLASSES = (
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
    'waffle.middleware.WaffleMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'plexus.urls'

TEMPLATE_DIRS = (
    "/var/www/plexus/templates/",
    os.path.join(os.path.dirname(__file__), "templates"),
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'django_nose',
    'compressor',
    'django_statsd',
    'bootstrapform',
    'lettuce.django',
    'template_utils',
    'plexus.main',
    'debug_toolbar',
    'smoketest',
    'django_jenkins',
    'waffle',
    'impersonate',
    'django_markwhat',
    'gunicorn',
    'storages',
]

INTERNAL_IPS = ('127.0.0.1', )
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
)

LETTUCE_APPS = (
    'plexus.main',
)


STATSD_CLIENT = 'statsd.client'
STATSD_PREFIX = 'plexus'
STATSD_HOST = '127.0.0.1'
STATSD_PORT = 8125

THUMBNAIL_SUBDIR = "thumbs"
EMAIL_SUBJECT_PREFIX = "[plexus] "
EMAIL_HOST = 'localhost'
SERVER_EMAIL = "plexus@ccnmtl.columbia.edu"
DEFAULT_FROM_EMAIL = SERVER_EMAIL

STATIC_ROOT = "/tmp/plexus/static"
STATICFILES_DIRS = ("media/",)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_URL = "/media/"
COMPRESS_ROOT = STATIC_ROOT

# WIND settings

CAS_BASE = "https://cas.columbia.edu/"
AUTHENTICATION_BACKENDS = ('djangowind.auth.SAMLAuthBackend',
                           'django.contrib.auth.backends.ModelBackend',)

#WIND_BASE = "https://wind.columbia.edu/"
#WIND_SERVICE = "cnmtl_full_np"
WIND_PROFILE_HANDLERS = ['djangowind.auth.CDAPProfileHandler']
WIND_AFFIL_HANDLERS = ['djangowind.auth.AffilGroupMapper',
                       'djangowind.auth.StaffMapper',
                       'djangowind.auth.SuperuserMapper']
WIND_STAFF_MAPPER_GROUPS = ['tlc.cunix.local:columbia.edu']
WIND_SUPERUSER_MAPPER_GROUPS = ['anp8', 'jb2410', 'zm4', 'egr2107', 'sld2131',
                                'amm8', 'mar227', 'jed2161', 'njn2118']

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True

HOSTMASTER_EMAIL = "hostmaster@columbia.edu"
SYSADMIN_LIST_EMAIL = "ccnmtl-sysadmin@columbia.edu"

GRAPHITE_BASE = "http://nanny.cul.columbia.edu/"
LOGIN_REDIRECT_URL = "/"
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
AWS_QUERYSTRING_AUTH = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}
