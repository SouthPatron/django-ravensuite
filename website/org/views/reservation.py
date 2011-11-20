from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.conf import settings

from singleobjectview import SingleObjectView
from listview import ListView

import uuid

from ..models import *
from common.utils.dbgdatetime import datetime

class ReservationList( ListView ):
	template_name = 'pages/org/reservation/index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Tab.objects.get( refnum = self.url_kwargs.tabid, client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid )


	def get_object_list( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'tabid' ], **kwargs )

		obj_list = Reservation.objects.filter( tab__refnum = mid.tabid, tab__client__refnum = mid.cid, tab__client__organization__refnum = mid.oid )
		return obj_list
	

	def create_object_json( self, request, data, *args, **kwargs ):
		amount = data.get( 'amount', 0 )

		if amount <= 0:
			return HttpResponseForbidden()

		duration = data.get( 'duration', 5 )

		if duration <= 1:
			return HttpResponseForbidden()


		mid = self._extract_ids( [ 'oid', 'cid', 'aid' ], **kwargs )

		# TODO: select_for_update()
		theaccount = Account.objects.get( refnum = mid.aid )

		if theaccount.is_enabled is False:
			return HttpResponseForbidden()

		newbal = theaccount.balance - theaccount.reserved - amount

		if newbal < theaccount.min_balance:
			return HttpResponseForbidden()

		expiry_action = data.get( 'expiry_action', ExpiryAction.ROLLBACK )
		if ExpiryAction.contains( expiry_action ) is False:
			return HttpResponseForbidden()


		res = Reservation()
		res.account = theaccount
		res.event_time = datetime.datetime.now()
		res.expiry_time = res.event_time + datetime.timedelta( minutes = duration )
		res.expiry_action = expiry_action
		res.group = data.get( 'group', '' )
		res.description = data.get( 'description', '' )

		if settings.DEBUG is True:
			res.uuid = '{}'.format( theaccount.transaction_no )
			theaccount.transaction_no += 1
		else:
			res.uuid = uuid.uuid4().hex

		res.amount = amount
		res.is_grouped = data.get( 'is_grouped', False )

		res.save()

		rdata = ReservationData.objects.create( reservation = res, data = data.get( 'data', '' ) )

		theaccount.reserved += amount
		theaccount.save()

		return redirect( 'org-client-tab-reservation-single', oid = mid.oid, cid = mid.cid, aid = mid.aid, rid = res.uuid )


class ReservationSingle( SingleObjectView ):
	template_name = 'pages/org/reservation/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'aid', 'rid' ], **kwargs )

		return get_object_or_404( Reservation, uuid = mid.rid, account__refnum = mid.aid, account__client__refnum = mid.cid, account__client__organization__refnum = mid.oid )

	def delete_object( self, request, ob, *args, **kwargs ):

		# TODO: select_for_update()
		theaccount = Account.objects.get( refnum = ob.account.refnum )
		theaccount.reserved -= ob.amount
		theaccount.save()

		ob.delete()
		return redirect( 'org-client-account-reservation-list', aid = ob.account.refnum, cid = ob.account.client.refnum, oid = ob.account.client.organization.refnum )


	def commit_reservation( self, request, obj, data, *args, **kwargs ):

		# TODO: select_for_update()
		theaccount = Account.objects.get( refnum = obj.account.refnum )

		amount = obj.amount

		newt = Transaction()
		newt.account = theaccount
		newt.refnum = theaccount.transaction_no
		newt.event_time = datetime.datetime.now()
		newt.group = data.get( 'group', obj.group )
		newt.description = data.get( 'description', obj.description )
		newt.is_grouped = data.get( 'group', obj.is_grouped )

		newt.balance_before = theaccount.balance
		newt.balance_reserved = theaccount.reserved - amount
		newt.balance_adjustment = -amount
		newt.balance_after = theaccount.balance - amount

		newt.save()

		tdata = TransactionData.objects.create( transaction = newt, data = data.get( 'data', obj.reservationdata.data ) )


		theaccount.balance -= amount
		theaccount.reserved -= amount

		theaccount.transaction_no += 1
		theaccount.save()

		obj.delete()

		return redirect( 'org-client-account-transaction-single', oid = theaccount.client.organization.refnum, cid = theaccount.client.refnum, aid = theaccount.refnum, tid = newt.refnum )
	

	def rollback_reservation( self, request, obj, data, *args, **kwargs ):
		return self.delete_object( request, obj, *args, **kwargs )
	
	def update_reservation( self, request, obj, data, *args, **kwargs ):
		if data.has_key( 'amount' ):
			return HttpResponseForbidden()

		duration = data.get( 'duration', None )
		if duration is not None and duration <= 1:
			return HttpResponseForbidden()


		expiry_action = data.get( 'expiry_action', ExpiryAction.ROLLBACK )
		if ExpiryAction.contains( expiry_action ) is False:
			return HttpResponseForbidden()

		obj.group = data.get( 'group', obj.group )
		obj.description = data.get( 'description', obj.description )
		obj.is_grouped = data.get( 'is_grouped', obj.is_grouped )
		obj.expiry_action = expiry_action

		if duration is not None:
			obj.expiry_time = datetime.datetime.now() + datetime.timedelta( minutes = duration )

		obj.save()

		if data.has_key( 'data' ):
			rdata = ReservationData.objects.get( reservation = obj )
			rdata.data = data.get( 'data' )
			rdata.save()

		return redirect( 'org-client-account-reservation-single', oid = obj.account.client.organization.refnum, cid = obj.account.client.refnum, aid = obj.account.refnum, rid = obj.uuid )



	def update_object_json( self, request, obj, data, *args, **kwargs ):

		action = data.get( 'action', 'update' )

		if action == 'commit':
			return self.commit_reservation( request, obj, data, *args, **kwargs )

		if action == 'rollback':
			return self.rollback_reservation( request, obj, data, *args, **kwargs )

		return self.update_reservation( request, obj, data, *args, **kwargs )
			



