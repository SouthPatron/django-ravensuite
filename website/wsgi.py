
try:
	from settings_local import *
except ImportError, e:
	pass

import os,sys
sys.path.append( WEBSITE_BASE )
sys.path.append( WEBSITE_BASE + '/website' )
os.environ.setdefault( "DJANGO_SETTINGS_MODULE", "website.settings")

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


