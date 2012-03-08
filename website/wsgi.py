import os,sys

WEBSITE_BASE = os.path.dirname( os.path.dirname( __file__ ) )

MODULE_NAME = 'website'

sys.path.append( WEBSITE_BASE )
sys.path.append( WEBSITE_BASE + '/' + MODULE_NAME )
os.environ.setdefault( "DJANGO_SETTINGS_MODULE", MODULE_NAME + '.settings' )

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


