# Django settings for southpatron project.

DEBUG = True
TEMPLATE_DEBUG = True

# --- These settings should be overriden in settings_local.py, especially
# --- the databases.

import os

SITE_ID = 1

WEBSITE_BASE = os.path.dirname( os.path.dirname( __file__ ) )

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': WEBSITE_BASE + '/db/southpatron.db',
			'USER': '',
		'PASSWORD': '',
		'HOST': '',
		'PORT': '',
	}
}

STATIC_BASE = WEBSITE_BASE + '/static'

TEMPLATE_DIRS = (
	WEBSITE_BASE + '/templates',
)



# --- Here comes the local stuff.

try:
	from settings_local import *
except ImportError, e:
	pass


