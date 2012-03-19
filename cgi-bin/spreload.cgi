#!/usr/bin/env python

import os

print 'Environment: {}'.format( os.environ )

try:
	if os.environ['mod_wsgi.process_group'] != '':
		import signal, os
		os.kill(os.getpid(), signal.SIGINT)
except KeyError, ke:
	print 'KeyError: {}'.format( ke.message )

