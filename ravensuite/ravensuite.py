from django.conf import settings

from slimit import minify

import os.path

import assets


def deploy_target( target ):
	dname = os.path.join( settings.STATIC_ROOT, target )

	src = os.path.dirname( os.path.realpath( __file__ ) )

	destination = open( dname, 'wb' )
	for fname in assets.assets[ target ][ 'files' ]:
		print 'minifying and concatenating ' + fname
		f = open( os.path.join( src, 'static', fname), 'rb')
		destination.write(
			minify( f.read(), mangle = True, mangle_toplevel = False )
		)
		f.close()
	destination.close()


def deploy():
	deploy_target( 'ravensuite-core.min.js' )



