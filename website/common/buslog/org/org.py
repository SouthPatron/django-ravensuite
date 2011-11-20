from common.models import *


class OrgBusLog( object ):

	@staticmethod
	def get_next_refnum():
		# TODO: select_for_update()
		sc = SystemCounter.objects.get( id = 1 )
		refnum = sc.organization_no
		sc.organization_no += 1
		sc.save()
		return refnum


	@staticmethod
	def create( trading_name ):

		refnum = OrgBusLog.get_next_refnum()

		neworg = Organization()
		neworg.trading_name = trading_name
		neworg.refnum = refnum
		neworg.save()

		OrganizationCounter.objects.create( organization = neworg )
		OrganizationAccount.objects.create( organization = neworg )

		return neworg



