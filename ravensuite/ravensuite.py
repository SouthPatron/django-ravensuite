from django.conf import settings

import shutil
import os.path

import assets


def combine_target( target ):
	dname = os.path.join( settings.STATIC_ROOT, target )

	src = os.path.dirname( os.path.realpath( __file__ ) )

	destination = open( dname, 'wb' )
	for fname in assets.assets[ target ][ 'files' ]:
		shutil.copyfileobj( open( os.path.join( src, 'static', fname), 'rb'), destination )
	destination.close()


def deploy():
	combine_target( 'ravensuite-core.js' )



