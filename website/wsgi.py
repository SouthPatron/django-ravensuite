import os,sys
sys.path.append( '/var/www/websites/southpatron.com' )
os.environ.setdefault( "DJANGO_SETTINGS_MODULE", "website.settings")


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


