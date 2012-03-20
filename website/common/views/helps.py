from __future__ import unicode_literals

from django.shortcuts import redirect

import signal, os


def restart( request ):
	os.kill(os.getpid(), signal.SIGINT)
	return redirect( '/' )




