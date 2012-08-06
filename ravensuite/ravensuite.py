import os.path

from django.conf import settings
from slimit import minify

import assets


def minify_and_concat( target, files ):
	destination = open( target, 'wb' )
	for fname in files:
		print 'minifying and concatenating ' + fname
		f = open( fname, 'rb')
		destination.write(
			minify( f.read(), mangle = True, mangle_toplevel = False )
		)
		f.close()
	destination.close()



def deploy_target( target, asset ):
	newlist = [ os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), 'static', fname ) for fname in assets.assets[ asset ]['files'] ]
	minify_and_concat(
		os.path.join( target, assets.assets[ asset ][ 'output' ] ),
		newlist
	)


def build():
	destdir = os.path.join( settings.STATIC_URL, 'scripts/ravensuite' )

	deploy_target( destdir, 'ravensuite-core' )




