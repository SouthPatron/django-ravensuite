from common.models import *


class UserBusLog( object ):

	@staticmethod
	def grant( user, org, category ):
		newuser = UserMembership()
		newuser.user = user
		newuser.organization = org
		newuser.category = category
		newuser.is_enabled = True
		newuser.save()



