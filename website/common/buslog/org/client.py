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
	def update( client, data ):
		client.trading_name = data.get( 'trading_name', client.trading_name )
		client.telephone_number = data.get( 'telephone_number', client.telephone_number )
		client.fax_number = data.get( 'fax_number', client.fax_number )
		client.email_address = data.get( 'email_address', client.email_address )
		client.postal_address = data.get( 'postal_address', client.postal_address )
		client.physical_address = data.get( 'physical_address', client.physical_address )


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

		ClientBusLog.update( newclient, data )

		newclient.save()


		account = Account()
		account.client = newclient
		account.balance = 0
		account.transaction_no = 1
		account.save()

		return newclient

