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
#	DATABASES = {
#		'default': {
#			'ENGINE': 'django.db.backends.sqlite3',
#			'NAME': '/home/user/db/southpatron.db',
# 			'USER': '',
#			'PASSWORD': '',
#			'HOST': '',
#			'PORT': '',
#		}
#	}
#
#	STATIC_BASE = '/home/user/projects/smk/products/southpatron/static'
#
#	TEMPLATE_DIRS = (
#		'/home/user/projects/smk/products/southpatron/templates',
#	)
#




