from __future__ import unicode_literals

from django.shortcuts import redirect


import signal, os


def restart( request ):
	try:
		if os.environ['mod_wsgi.process_group'] != '':
			os.kill(os.getpid(), signal.SIGINT)
	except KeyError, ke:
		pass
	return redirect( '/' )




