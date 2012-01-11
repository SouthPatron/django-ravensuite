from __future__ import unicode_literals

from django.db.models import F

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseServerError
from django.contrib import messages

from common.views.singleobjectview import SingleObjectView
from common.views.listview import ListView
from common.views.component import ComponentView 

from common.buslog.org import InvoiceBusLog, PaymentBusLog

from common.exceptions import *
from common.models import *


class InvoiceList( ListView ):
	template_name = 'pages/org/invoice/index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = ItemListTransaction.objects.filter( client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid, document_type = ItemListType.INVOICE )
		return obj_list

	def _create_object( self, request, data, *args, **kwargs ):
		client = Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )
		newo = InvoiceBusLog.create( client )
		return newo
		
	
	def create_object_html( self, request, data, *args, **kwargs ):

		client = Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

		try:
			newo = self._create_object( request, data, *args, **kwargs )
		except BusLogError, berror:
			messages.error( request, berror.message )
			return redirect( client.get_invoice_list_url() )
		except Exception, error:
			print error

		return redirect( newo.get_single_url() )


	def create_object_json( self, request, data, *args, **kwargs ):
		newo = self._create_object( request, data, *args, **kwargs )
		resp = { 'url' : newo.get_single_url() }
		return self.api_resp( resp )


class InvoiceDraftList( ListView ):
	template_name = 'pages/org/invoice/draft-index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = ItemListTransaction.objects.filter( client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid, document_type = ItemListType.INVOICE, document_state = ItemListState.DRAFT )
		return obj_list


class InvoiceUnpaidList( ListView ):
	template_name = 'pages/org/invoice/unpaid-index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = ItemListTransaction.objects.filter( client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid, document_type = ItemListType.INVOICE, document_state = ItemListState.FINAL, total__gt = F('allocated') )
		return obj_list



class InvoiceSingle( SingleObjectView ):
	template_name = 'pages/org/invoice/single'

	def get_object( self, request, *args, **kwargs ):
		obj = get_object_or_404( ItemListTransaction, refnum = self.url_kwargs.ilid, client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid )

		if obj.document_state == ItemListState.DRAFT:
			self.template_name = 'pages/org/invoice/single-draft'
		elif obj.document_state == ItemListState.FINAL:
			self.template_name = 'pages/org/invoice/single-final'
		elif obj.document_state == ItemListState.VOID:
			self.template_name = 'pages/org/invoice/single-void'

		return obj

	def delete_object( self, request, ob, *args, **kwargs ):
		InvoiceBusLog.delete( ob )
		return redirect( ob.get_client().get_invoice_list_url() )


	def update_object_html( self, request, obj, data, *args, **kwargs ):

		invoice_data = {}

		invoice_data[ 'state' ] = data.get( 'invoice_state' )

		if invoice_data[ 'state' ] is not None and long(invoice_data['state']) == ItemListState.DELETE:
			rc = self.delete_object( request, obj, *args, **kwargs )
			messages.info( request, 'The draft invoice has been deleted' )
			return redirect( obj.get_client().get_draft_invoice_list_url() )

		invoice_data[ 'invoice_date' ] = data.get( 'invoice_date' )
		invoice_data[ 'due_date' ] = data.get( 'due_date' )
		invoice_data[ 'tax' ] = data.get( 'invoice_tax' )
		invoice_data[ 'amount' ] = data.get( 'invoice_amount' )
		invoice_data[ 'total' ] = data.get( 'invoice_total' )
		invoice_data[ 'comment' ] = data.get( 'invoice_comment', "" )
		invoice_data[ 'items' ] = []
		
		for pos in range( len(data.getlist( 'description' )) ):
			invoice_data[ 'items' ].append( [
						data.getlist( 'description' )[ pos ],
						data.getlist( 'units' )[ pos ],
						data.getlist( 'perunit' )[ pos ],
						data.getlist( 'tax_rate' )[ pos ],
						data.getlist( 'amount' )[ pos ]
					] )

		try:
			InvoiceBusLog.update( obj, invoice_data )
		except BusLogError, berror:
			messages.error( request, berror.message )
			return redirect( obj.get_single_url() )

		if obj.document_state == ItemListState.DRAFT:
			return redirect( obj.get_client().get_draft_invoice_list_url() )
	
		return redirect( obj.get_client().get_account_single_url() )


	def update_object_json( self, request, obj, data, *args, **kwargs ):

		newstate = data.get( 'state', None )

		if newstate is not None:
			if ItemListState.contains( newstate ) is False:
				return HttpResponseForbidden()

			if obj.document_state == ItemListState.FINAL:
				if newdocument_state != ItemListState.VOID:
					return HttpResponseForbidden()
				return void_invoice( request, obj, data, *args, **kwargs )

			if newdocument_state == ItemListState.VOID:
				return delete_object( request, obj, data, *args, **kwargs )

			if newdocument_state == ItemListState.FINAL:
				return finalize_invoice( request, obj, data, *args, **kwargs )

			return HttpResponseServerError()

		return update_invoice( request, obj, data, *args, **kwargs )



class InvoiceComponents( ComponentView ):

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404(
					ItemListTransaction,
					refnum = self.url_kwargs.ilid,
					client__refnum = self.url_kwargs.cid,
					client__organization__refnum = self.url_kwargs.oid
				)

class IcAllocatePayment( InvoiceComponents ):
	template_name = 'components/org/invoice/allocate_payment'

	def post_html( self, request, obj, data, *args, **kwargs ):

		payment_refnum = data.get( "payment-refnum" )
		payment_amount = data.get( "payment-amount" )

		# TODO: Select for update somehow
		payment = get_object_or_404(
						Payment,
						refnum = payment_refnum,
						client__refnum = obj.get_client().refnum
					)

		try:
			PaymentBusLog.allocate( payment, obj, payment_amount )
		except BusLogError, berror:
			messages.error( request, berror.message )
			return redirect( obj.get_single_url() )

		messages.success( request, 'Successfully allocated.' )

		return redirect( obj.get_single_url() )


class IcDeallocatePayment( InvoiceComponents ):
	template_name = 'components/org/invoice/deallocate_payment'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404(
					PaymentAllocation,
					id = request.GET[ 'payid' ],
					invoice__refnum = self.url_kwargs.ilid
				)


	def post_html( self, request, obj, data, *args, **kwargs ):

		try:
			PaymentBusLog.deallocate( obj )
		except BusLogError, berror:
			messages.error( request, berror.message )
			return redirect( obj.invoice.get_single_url() )

		messages.success( request, 'Successfully deallocated.' )
		return redirect( obj.invoice.get_single_url() )





