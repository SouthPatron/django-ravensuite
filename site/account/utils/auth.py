from common.utils.dbgdatetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


class AuthBusLog( object ):

	@staticmethod
	def login( request, username, password ):
		user = authenticate( username = username, password = password )
		login( request, user )

		prof = user.get_profile()
		prof.last_seen = datetime.datetime.now()
		prof.save()

	@staticmethod
	def logout( request ):
		logout( request )


