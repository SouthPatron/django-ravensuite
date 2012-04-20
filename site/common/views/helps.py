import signal, os

from django.shortcuts import redirect

def restart( request ):
	os.kill(os.getpid(), signal.SIGINT)
	return redirect( '/' )

