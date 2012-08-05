from django.conf import settings

import shutil
import os.path

import assets



def combine_target( target ):
	dname = os.path.join( settings.STATIC_ROOT, target )

	destination = open( dname, 'wb' )
	for fname in assets.assets[ target ][ 'files' ]:
		shutil.copyfileobj( open( os.path.join('/static/',fname), 'rb'), destination)
	destination.close()



def deploy():
	build_ravensuite_js( 'ravensuite-core.js' )



