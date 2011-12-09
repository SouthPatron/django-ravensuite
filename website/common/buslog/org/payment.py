from __future__ import unicode_literals

from math import *
from copy import deepcopy

from common.models import *
from common.exceptions import *
from common.buslog.org import AccountBusLog
from common.moe import MarginsOfError
from common.utils.dbgdatetime import datetime


class PaymentBusLog( object ):

	@staticmethod
	def get_next_refnum( org ):
		# TODO: select_for_update()
		sc = OrganizationCounter.objects.get( organization__refnum = org.refnum )
		refnum = sc.payment_no
		sc.payment_no += 1
		sc.save()
		return refnum

	@staticmethod
	def _create_sanitize_dates( new_data ):
		try:
			new_data[ 'payment_date' ] = datetime.datetime.strptime( new_data[ 'payment_date' ], '%d %b %Y' )
		except ValueError:
			raise BusLogError( 'The payment date is invalid' )


	@staticmethod
	def _create_sanitize_amount( new_data ):
		nn = new_data.get( 'amount', 0 )
		if nn <= 0:
			raise BusLogError( 'The payment amount is invalid.' )
		new_data[ 'amount' ] = long(float(nn) * 100)


	@staticmethod
	def _create_sanitize( data ):
		PaymentBusLog._create_sanitize_dates( data )
		PaymentBusLog._create_sanitize_amount( data )


	@staticmethod
	def create( client, data ):

		new_data = deepcopy( data )

		PaymentBusLog._create_sanitize( new_data )

		newt = Payment()
		newt.client = client
		newt.refnum = PaymentBusLog.get_next_refnum( client.get_org() )
		newt.creation_time = datetime.datetime.now()
		newt.payment_date = new_data[ 'payment_date' ]
		newt.amount = new_data[ 'amount' ]
		newt.comment = new_data.get( 'comment', '' )
		newt.is_allocated = False
		newt.state = PaymentState.ACTIVE
		newt.save()

		transaction = AccountBusLog.adjust(
				newt.client.account,
				'PAYMENT',
				'Payment {} Received'.format( newt.refnum ),
				newt.amount,
				''
			)

		return newt


	@staticmethod
	def void( payment ):
		transaction = AccountBusLog.adjust(
				payment.client.account,
				'VOID',
				'Void of Payment {}'.format( payment.refnum ),
				float(0) - payment.total,
				''
			)
