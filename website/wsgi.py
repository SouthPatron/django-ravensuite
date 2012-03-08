import os,sys

WEBSITE_BASE = os.path.dirname( os.path.dirname( __file__ ) )

sys.path.append( WEBSITE_BASE )
sys.path.append( WEBSITE_BASE + '/' + __name__ )
os.environ.setdefault( "DJANGO_SETTINGS_MODULE", __name__ + '.settings' )

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


