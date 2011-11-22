from common.models import *

from common.exceptions import *

from common.buslog.account import AccountSupport
from common.utils.email import send_templated_email


class UserBusLog( object ):

	@staticmethod
	def grant( user, org, category ):

		if UserMembership.objects.filter( user = user, organization = org ).exists():
			raise BusLogError( 'That user already has access to this organization.' )

		if UserMembership.objects.filter( user = user, organization__trading_name = org.trading_name ).exists() is True:
			raise BusLogError( 'That user already has an organization with the same name as this one. One of them will need to change names.' )

		newuser = UserMembership()
		newuser.user = user
		newuser.organization = org
		newuser.category = category
		newuser.is_enabled = True
		newuser.save()

		return newuser


	@staticmethod
	def invite_user( first_name, last_name, email_address, org, category ):

		wasNewUser = False

		try:
			the_user = User.objects.get( email = email_address )
		except User.DoesNotExist:
			new_password = User.objects.make_random_password()
			the_user = AccountSupport.create( email_address, new_password, first_name, last_name )
			wasNewUser = True

		newgrant = UserBusLog.grant( the_user, org, category )

		if wasNewUser is True:
			send_templated_email( the_user, 'org', 'user_added', { 'password' : new_password, 'organization' : org } )

		return newgrant


