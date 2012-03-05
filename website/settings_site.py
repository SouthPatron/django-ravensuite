# Django settings for southpatron project.

DEBUG = True
TEMPLATE_DEBUG = True


try:
	from settings_local import *
except ImportError, e:
	pass


# --- These settings should be overriden in settings_local.py
#
#	SITE_ID = 1
#
#	WEBSITE_BASE = '/home/user/projects/smk/products/southpatron'
#
#	DATABASES = {
#		'default': {
#			'ENGINE': 'django.db.backends.sqlite3',
#			'NAME': WEBSITE_BASE + '/db/southpatron.db',
# 			'USER': '',
#			'PASSWORD': '',
#			'HOST': '',
#			'PORT': '',
#		}
#	}
#
#	STATIC_BASE = WEBSITE_BASE + '/static'
#
#	TEMPLATE_DIRS = (
#		WEBSITE_BASE + '/templates',
#	)
#

