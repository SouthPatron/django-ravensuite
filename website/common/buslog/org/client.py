from __future__ import unicode_literals

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
	def create( org, trading_name ):

		try:
			newclient = Client.objects.get( trading_name = trading_name, organization = org )

			raise BLE_ConflictError( 'There is already a client with that name.' )
		except Client.DoesNotExist:
			pass


		refnum = ClientBusLog.get_next_refnum( org )

		newclient = Client()
		newclient.organization = org
		newclient.refnum = refnum
		newclient.trading_name = trading_name
		newclient.save()

		account = Account()
		account.client = newclient
		account.balance = 0
		account.transaction_no = 1
		account.save()

		return newclient

