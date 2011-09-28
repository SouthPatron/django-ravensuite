from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect


from django.http import HttpResponseForbidden

from singleobjectview import SingleObjectView
from listview import ListView

import uuid

from ..models import *
from ..utils.dbgdatetime import datetime

class ReservationList( ListView ):
	template_name = 'pages/org/reservation/index'

	def get_object_list( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'aid' ], **kwargs )

		obj_list = Reservation.objects.filter( account = mid.aid, account__client = mid.cid, account__client__organization = mid.oid )
		return obj_list
	
	def create_object_json( self, request, data, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'aid' ], **kwargs )

		amount = data[ 'amount' ]

		if amount <= 0:
			return HttpResponseForbidden()

		# TODO: select_for_update()
		theaccount = Account.objects.get( refnum = mid.aid )

		newbal = theaccount.balance - theaccount.reserved - amount

		if newbal < theaccount.min_balance:
			return HttpResponseForbidden()

		res = Reservation()
		res.account = theaccount
		res.event_time = datetime.datetime.now()
		res.expiry_time = datetime.datetime.now()
		res.group = data.get( 'group', '' )
		res.description = data.get( 'description', '' )
		res.is_grouped = data.get( 'is_grouped', False )

		res.uuid = uuid.uuid4().hex
		res.amount = amount

		res.save()

		theaccount.reserved += amount
		theaccount.save()

		return redirect( 'org-client-account-reservation-single', oid = mid.oid, cid = mid.cid, aid = mid.aid, rid = res.uuid )


class ReservationSingle( SingleObjectView ):
	template_name = 'pages/org/reservation/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'aid', 'rid' ], **kwargs )

		return get_object_or_404( Reservation, uuid = mid.rid, account__refnum = mid.aid, account__client = mid.cid, account__client__organization = mid.oid )



