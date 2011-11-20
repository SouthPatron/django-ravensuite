import datetime

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout



class AuthBusLog( object ):

	@staticmethod
	def login( request, username, password ):
		user = authenticate( username = username, password = password )
		login( request, user )

	@staticmethod
	def logout( request ):
		logout( request )


