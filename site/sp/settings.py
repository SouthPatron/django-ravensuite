# Django settings for southpatron project.

DEBUG = False
TEMPLATE_DEBUG = False

WSGI_APPLICATION = "sp.wsgi.application"

AUTH_PROFILE_MODULE = "common.UserProfile"

LOGIN_URL = '/v/account/login'
LOGOUT_URL = '/v/account/logout'
LOGIN_REDIRECT_URL = '/v/org/'

SEND_BROKEN_LINK_EMAILS = True


TIME_ZONE = 'UTC'
USE_TZ=True


USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en-us'

ugettext = lambda s: s
LANGUAGES = (
	('en', ugettext('English')),
)


MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_URL = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ffcx$@3767*we0o*t+xxk=is3@f&=!si=v^p-1h@3e!fe27k^r'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.transaction.TransactionMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'sp.urls'


TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.static',
	'django.contrib.messages.context_processors.messages',

	# Hereforth, non-default context processors
	'django.core.context_processors.request',
)


INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.flatpages',
	'django.contrib.messages',

	'django.contrib.admin',
	'django.contrib.admindocs',

	'south',

	'common',

	'sp.api',

	'sp.account',
	'sp.org',
)


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,

	'formatters': {
		'verbose': {
			'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
		},
		'simple': {
			'format': '%(levelname)s %(message)s'
		},
	},

	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},

	'handlers': {
		'console':{
			'level':'INFO',
			'class':'logging.StreamHandler',
			'formatter': 'simple'
		},
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		}
	},

	'loggers': {
		'': {
			'handlers': [ 'console' ],
			'level': 'INFO',
			'propagate': True,
		},

		'django.request': {
			'handlers': [ 'mail_admins' ],
			'level': 'ERROR',
			'propagate': True,
		},
	}
}


# Load site specific configurations

try:
	from settings_site import *
except ImportError, e:
	pass


