from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect


from django.http import HttpResponseForbidden

from singleobjectview import SingleObjectView
from listview import ListView

from ..models import *
from ..utils.dbgdatetime import datetime

class TransactionList( ListView ):
	template_name = 'pages/org/transaction/index'

	def get_object_list( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'aid' ], **kwargs )

		obj_list = Transaction.objects.filter( account = mid.aid, account__client = mid.cid, account__client__organization = mid.oid )
		return obj_list
	
	def create_object_json( self, request, data, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'aid' ], **kwargs )

		amount = data[ 'amount' ]

		# TODO: select_for_update()
		theaccount = Account.objects.get( refnum = mid.aid )

		newbal = theaccount.balance - theaccount.reserved + amount

		if newbal < theaccount.min_balance:
			return HttpResponseForbidden()

		newt = Transaction()
		newt.account = theaccount
		newt.event_time = datetime.datetime.now()
		newt.group = data.get( 'group', '' )
		newt.description = data.get( 'description', '' )

		newt.balance_before = theaccount.balance
		newt.balance_adjustment = amount
		newt.balance_after = theaccount.balance + amount

		newt.is_grouped = data.get( 'is_grouped', False )
		newt.is_voided = data.get( 'is_voided', False )
		newt.save()

		tdata = TransactionData.objects.create( transaction = newt, data = data.get( 'data', '' ) )

		theaccount.balance += amount
		theaccount.save()

		refnum = newt.id

		return redirect( 'org-client-account-transaction-single', oid = mid.oid, cid = mid.cid, aid = mid.aid, tid = refnum )


class TransactionSingle( SingleObjectView ):
	template_name = 'pages/org/transaction/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'aid', 'tid' ], **kwargs )

		return get_object_or_404( Transaction, id = mid.tid, account__refnum = mid.aid, account__client = mid.cid, account__client__organization = mid.oid )



