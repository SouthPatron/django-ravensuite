import datetime

from ..models import *


class AccountSupport( object ):

	@staticmethod
	def get_next_refnum():
		# TODO: select_for_update()
		sc = SystemCounter.objects.get( id = 1 )
		refnum = sc.profile_no
		sc.profile_no += 1
		sc.save()
		return refnum


	@staticmethod
	def create( username, password, firstname, lastname ):
		luser = User.objects.create_user( username, username, password )
		luser.first_name = firstname
		luser.last_name = lastname
		luser.email = username
		luser.is_active = True
		luser.save()

		luser_profile = UserProfile( user = luser )
		luser_profile.refnum = AccountSupport.get_next_refnum()
		luser_profile.state = ProfileState.UNAUTHENTICATED
		luser_profile.creation_time = datetime.datetime.now()
		luser_profile.save()

		lauth_code = AuthenticationCode( user = luser, authentication_code = User.objects.make_random_password(), creation_time = datetime.datetime.now() )
		lauth_code.save()

		return luser

	@staticmethod
	def authenticate( user ):
		profile = user.get_profile()
		profile.state = ProfileState.ACTIVE
		profile.save()


