import os.path

from django.conf import settings
from slimit import minify

import assets

def minify_and_concat( target, files, append = False, minify = True ):
	mode = 'wb'
	if append is True:
		mode = 'ab'

	destination = open( target, mode )
	for fname in files:
		print 'minifying and concatenating ' + fname
		f = open( fname, 'rb')
		if minify is True:
			destination.write(
				minify( f.read(), mangle = True, mangle_toplevel = False )
			)
		else:
			destination.write( f.read() )

		f.close()
	destination.close()


def build_asset( destdir, asset ):

	target = os.path.join( destdir, assets.assets[ asset ][ 'output' ] )

	destination = open( target, 'wb' )

	for jsname in assets.assets[ asset ]['order']:

		isMax = False

		try:
			fname = assets.assets[ asset ][ 'min_files' ][ jsname ]
		except KeyError, ke:
			fname = assets.assets[ asset ][ 'max_files' ][ jsname ]
			isMax = True


		newname = os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), 'static', fname )

		f = open( fname, 'rb')
		if isMax is True:
			print 'minifying and concatenating ' + fname
			destination.write(
				minify( f.read(), mangle = True, mangle_toplevel = False )
			)
		else:
			print 'concatenating ' + fname
			destination.write( f.read() )

		f.close()

	destination.close()


def build():
	destdir = os.path.join(
				settings.STATIC_ROOT,
				'scripts/ravensuite'
			)

	build_asset( destdir, 'ravensuite-core' )




