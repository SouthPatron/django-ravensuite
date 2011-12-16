from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseServerError
from django.contrib import messages

from common.views.singleobjectview import SingleObjectView
from common.views.listview import ListView
from common.views.component import ComponentView

from common.buslog.org import PaymentBusLog

from common.exceptions import *
from common.models import *


class PaymentList( ListView ):
	template_name = 'pages/org/payment/index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = Payment.objects.filter( client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid )
		return obj_list

	def _create_object( self, request, data, *args, **kwargs ):
		client = Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )
		newo = PaymentBusLog.create( client, data )
		return newo
		
	
	def create_object_html( self, request, data, *args, **kwargs ):
		client = Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

		try:
			newo = self._create_object( request, data, *args, **kwargs )
		except BusLogError, berror:
			messages.error( request, berror.message )
			return redirect( client.get_account_single_url() )

		return redirect( newo.get_single_url() )


	def create_object_json( self, request, data, *args, **kwargs ):
		newo = self._create_object( request, data, *args, **kwargs )
		resp = { 'url' : newo.get_single_url() }
		return self.api_resp( resp )


class PaymentUnallocatedList( PaymentList ):
	template_name = 'pages/org/payment/index'

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = Payment.objects.filter( client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid, is_allocated = False )
		return obj_list


class PaymentComponents( ComponentView ):

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404(
					Payment,
					refnum = self.url_kwargs.payid,
					client__refnum = self.url_kwargs.cid,
					client__organization__refnum = self.url_kwargs.oid
				)



class PcAllocatePayment( PaymentComponents ):
	template_name = 'components/org/payment/allocate_payment'

	def post_html( self, request, obj, data, *args, **kwargs ):

		invoice_refnum = data.get( "invoice-refnum" )
		payment_amount = data.get( "payment-amount" )

		# TODO: Select for update somehow
		invoice = get_object_or_404(
						Invoice,
						refnum = invoice_refnum,
						client__refnum = obj.get_client().refnum
					)

		try:
			PaymentBusLog.allocate( obj, invoice, payment_amount )
		except BusLogError, berror:
			messages.error( request, berror.message )
			return redirect( obj.get_single_url() )

		messages.success( request, 'Successfully allocated.' )

		return redirect( obj.get_single_url() )




class PaymentSingle( SingleObjectView ):
	template_name = 'pages/org/payment/single'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Payment, refnum = self.url_kwargs.payid, client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid )



