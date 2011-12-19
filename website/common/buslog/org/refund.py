from __future__ import unicode_literals

from math import *
from copy import deepcopy

from common.models import *
from common.exceptions import *
from common.buslog.org import AccountBusLog
from common.utils.dbgdatetime import datetime
from common.utils.objroute import ObjRoute


class RefundBusLog( object ):

	@staticmethod
	def get_next_refnum( org ):
		# TODO: select_for_update()
		sc = OrganizationCounter.objects.get( organization__refnum = org.refnum )
		refnum = sc.refund_no
		sc.refund_no += 1
		sc.save()
		return refnum

	@staticmethod
	def _create_sanitize_dates( new_data ):
		try:
			new_data[ 'refund_date' ] = datetime.datetime.strptime( new_data[ 'refund_date' ], '%d %b %Y' )
		except ValueError:
			raise BusLogError( 'The refund date is invalid' )


	@staticmethod
	def _create_sanitize_amount( new_data ):
		nn = new_data.get( 'amount', 0 )
		if nn <= 0:
			raise BusLogError( 'The refund amount is invalid.' )
		new_data[ 'amount' ] = long(float(nn) * 100)


	@staticmethod
	def _create_sanitize( data ):
		RefundBusLog._create_sanitize_dates( data )
		RefundBusLog._create_sanitize_amount( data )


	@staticmethod
	def create( client, data ):

		# TODO: Lock account balance while busy

		new_data = deepcopy( data )

		RefundBusLog._create_sanitize( new_data )

		amt = new_data[ 'amount' ]

		if client.account.balance - amt < 0:
			raise BusLogError( 'That refund would put the account into the negative. Please raise a credit note for the difference and try again.' )


		newt = Refund()
		newt.client = client
		newt.refnum = RefundBusLog.get_next_refnum( client.get_org() )
		newt.creation_time = datetime.datetime.now()
		newt.refund_date = new_data[ 'refund_date' ]
		newt.amount = amt
		newt.comment = new_data.get( 'comment', '' )
		newt.state = RefundState.ACTIVE
		newt.save()

		transaction = AccountBusLog.adjust(
				newt.client.account,
				'REFUND',
				'Refund {} Given'.format( newt.refnum ),
				float(0) - newt.amount,
				ObjRoute.gen( newt ),
				''
			)

		return newt


	@staticmethod
	def void( refund ):
		transaction = AccountBusLog.adjust(
				refund.client.account,
				'VOID',
				'Void of Refund {}'.format( refund.refnum ),
				refund.amount,
				ObjRoute.gen( refund ),
				''
			)

		refund.state = RefundState.VOID
		refund.save()


