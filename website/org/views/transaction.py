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

		obj_list = Transaction.objects.filter( account__refnum = mid.aid, account__client__refnum = mid.cid, account__client__organization__refnum = mid.oid )
		return obj_list
	
	def create_object_json( self, request, data, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'aid' ], **kwargs )

		amount = data[ 'amount' ]

		# TODO: select_for_update()
		theaccount = Account.objects.get( refnum = mid.aid )

		if theaccount.is_enabled is False:
			return HttpResponseForbidden()

		newbal = theaccount.balance - theaccount.reserved + amount

		if newbal < theaccount.min_balance:
			return HttpResponseForbidden()

		newt = Transaction()
		newt.account = theaccount
		newt.refnum = theaccount.transaction_no
		newt.event_time = datetime.datetime.now()
		newt.group = data.get( 'group', '' )
		newt.description = data[ 'description' ]

		newt.balance_before = theaccount.balance
		newt.balance_reserved = theaccount.reserved
		newt.balance_adjustment = amount
		newt.balance_after = theaccount.balance + amount

		newt.is_grouped = data.get( 'is_grouped', False )
		newt.save()

		tdata = TransactionData.objects.create( transaction = newt, data = data.get( 'data', '' ) )

		theaccount.balance += amount
		theaccount.transaction_no += 1
		theaccount.save()

		return redirect( 'org-client-account-transaction-single', oid = mid.oid, cid = mid.cid, aid = mid.aid, tid = newt.refnum )


class TransactionSingle( SingleObjectView ):
	template_name = 'pages/org/transaction/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'aid', 'tid' ], **kwargs )
		return get_object_or_404( Transaction, refnum = mid.tid, account__refnum = mid.aid, account__client__refnum = mid.cid, account__client__organization__refnum = mid.oid )


	def update_object_json( self, request, obj, data, *args, **kwargs ):
		if data.has_key( 'amount' ):
			return HttpResponseForbidden()

		obj.group = data.get( 'group', obj.group )
		obj.description = data.get( 'description', obj.description )
		obj.is_grouped = data.get( 'is_grouped', obj.is_grouped )
		obj.save()

		if data.has_key( 'data' ):
			tdata = TransactionData.objects.get( transaction = obj )
			tdata.data = data.get( 'data' )
			tdata.save()

		return redirect( 'org-client-account-transaction-single', oid = obj.account.client.organization.refnum, cid = obj.account.client.refnum, aid = obj.account.refnum, tid = obj.refnum )



