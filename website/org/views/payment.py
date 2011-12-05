from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseServerError
from django.contrib import messages

from common.views.singleobjectview import SingleObjectView
from common.views.listview import ListView

from common.buslog.org import PaymentBusLog

from common.exceptions import *
from common.models import *


class PaymentList( ListView ):
	template_name = 'pages/org/payment/index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid' ], **kwargs )

		obj_list = Payment.objects.filter( client__refnum = mid.cid, client__organization__refnum = mid.oid )
		return obj_list

	def _create_object( self, request, data, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid' ], **kwargs )
		client = Client.objects.get( refnum = mid.cid, organization__refnum = mid.oid )
		newo = PaymentBusLog.create( client, data )
		return newo
		
	
	def create_object_html( self, request, data, *args, **kwargs ):

		mid = self._extract_ids( [ 'oid', 'cid' ], **kwargs )
		client = Client.objects.get( refnum = mid.cid, organization__refnum = mid.oid )

		try:
			newo = self._create_object( request, data, *args, **kwargs )
		except BusLogError, berror:
			messages.error( request, berror.message )
			return redirect( client.get_payment_list_url() )

		return redirect( newo.get_single_url() )


	def create_object_json( self, request, data, *args, **kwargs ):
		newo = self._create_object( request, data, *args, **kwargs )
		resp = { 'url' : newo.get_single_url() }
		return self.api_resp( resp )


class PaymentSingle( SingleObjectView ):
	template_name = 'pages/org/payment/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'payid' ], **kwargs )
		return get_object_or_404( Payment, refnum = mid.payid, client__refnum = mid.cid, client__organization__refnum = mid.oid )



