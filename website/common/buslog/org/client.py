from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from common.models import *
from common.exceptions import *


class ClientBusLog( object ):

	@staticmethod
	def get_next_refnum( org ):
		# TODO: make safe in case two are created
		sc = org.organizationcounter
		refnum = sc.client_no
		sc.client_no += 1
		sc.save()
		return refnum


	@staticmethod
	def create( org, data ):

		try:
			newclient = Client.objects.get( trading_name = data[ 'trading_name' ], organization = org )

			raise BLE_ConflictError( _('BLE_50002') )
		except Client.DoesNotExist:
			pass


		refnum = ClientBusLog.get_next_refnum( org )

		newclient = Client()
		newclient.organization = org
		newclient.refnum = refnum
		newclient.trading_name = data[ 'trading_name' ]
		newclient.telephone_number = data.get( 'telephone_number', '' )
		newclient.fax_number = data.get( 'fax_number', '' )
		newclient.email_address = data.get( 'email_address', '' )
		newclient.postal_address = data.get( 'postal_address', '' )
		newclient.physical_address = data.get( 'physical_address', '' )
		newclient.save()


		account = Account()
		account.client = newclient
		account.balance = 0
		account.transaction_no = 1
		account.save()

		return newclient

