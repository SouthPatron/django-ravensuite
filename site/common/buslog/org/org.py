
from django.utils.translation import ugettext as _

from common.exceptions import *
from common.models import *


class OrgBusLog( object ):

	@staticmethod
	def get_next_refnum():
		sc = SystemCounter.objects.select_for_update().get( id = 1 )
		refnum = sc.organization_no
		sc.organization_no += 1
		sc.save()
		return refnum

	@staticmethod
	def update( org, data ):
		org.trading_name = data.get( 'trading_name', org.trading_name )
		org.telephone_number = data.get( 'telephone_number', org.telephone_number )
		org.fax_number = data.get( 'fax_number', org.fax_number )
		org.email_address = data.get( 'email_address', org.email_address )
		org.postal_address = data.get( 'postal_address', org.postal_address )
		org.physical_address = data.get( 'physical_address', org.physical_address )



	@staticmethod
	def create( user, data ):

		try:
			neworg = Organization.objects.get( trading_name = data[ 'trading_name' ], usermembership__user = user )

			raise BLE_ConflictError( _('BLE_50003') )
		except Organization.DoesNotExist:
			pass

		refnum = OrgBusLog.get_next_refnum()

		neworg = Organization()
		neworg.refnum = refnum

		OrgBusLog.update( neworg, data )

		neworg.save()

		OrganizationCounter.objects.create( organization = neworg )
		OrganizationAccount.objects.create( organization = neworg )

		return neworg



