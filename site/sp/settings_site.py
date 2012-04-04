# Django settings for southpatron project.

DEBUG = True
TEMPLATE_DEBUG = True

# --- These settings should be overriden in settings_local.py, especially
# --- the databases.

import os
from os.path import dirname

SITE_ID = 1

WEBSITE_BASE = dirname( dirname( dirname( __file__ ) ) )

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'southpatron',
		'USER': 'postgres',
		'PASSWORD': '',
		'HOST': '',
		'PORT': '',
	}
}

STATIC_BASE = WEBSITE_BASE + '/static/static'

TEMPLATE_DIRS = (
	WEBSITE_BASE + '/templates',
	WEBSITE_BASE + '/templates/errors',
)


ADMINS = (
	( 'Support at South Patron', 'support@southpatron.com' ),
)

MANAGERS = ADMINS



# --- Here comes the local stuff.

try:
	from settings_local import *
except ImportError, e:
	pass


