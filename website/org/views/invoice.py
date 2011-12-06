from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseServerError
from django.contrib import messages

from common.views.singleobjectview import SingleObjectView
from common.views.listview import ListView

from common.buslog.org import InvoiceBusLog

from common.exceptions import *
from common.models import *


class InvoiceList( ListView ):
	template_name = 'pages/org/invoice/index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid' ], **kwargs )

		obj_list = Invoice.objects.filter( client__refnum = mid.cid, client__organization__refnum = mid.oid )
		return obj_list

	def _create_object( self, request, data, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid' ], **kwargs )
		client = Client.objects.get( refnum = mid.cid, organization__refnum = mid.oid )
		newo = InvoiceBusLog.create( client )
		return newo
		
	
	def create_object_html( self, request, data, *args, **kwargs ):

		mid = self._extract_ids( [ 'oid', 'cid' ], **kwargs )
		client = Client.objects.get( refnum = mid.cid, organization__refnum = mid.oid )

		try:
			newo = self._create_object( request, data, *args, **kwargs )
		except BusLogError, berror:
			messages.error( request, berror.message )
			return redirect( client.get_invoice_list_url() )

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
		mid = self._extract_ids( [ 'oid', 'cid' ], **kwargs )
		obj_list = Invoice.objects.filter( client__refnum = mid.cid, client__organization__refnum = mid.oid, state = InvoiceState.DRAFT )
		return obj_list




class InvoiceSingle( SingleObjectView ):
	template_name = 'pages/org/invoice/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'iid' ], **kwargs )
		return get_object_or_404( Invoice, refnum = mid.iid, client__refnum = mid.cid, client__organization__refnum = mid.oid )

	def delete_object( self, request, ob, *args, **kwargs ):
		InvoiceBusLog.delete( ob )
		return redirect( ob.get_client().get_invoice_list_url() )


	def update_object_html( self, request, obj, data, *args, **kwargs ):

		invoice_data = {}

		invoice_data[ 'state' ] = data.get( 'invoice_state' )

		if long(invoice_data['state']) == InvoiceState.DELETE:
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
	
		return redirect( obj.get_client().get_draft_invoice_list_url() )


	def update_object_json( self, request, obj, data, *args, **kwargs ):

		newstate = data.get( 'state', None )

		if newstate is not None:
			if InvoiceState.contains( newstate ) is False:
				return HttpResponseForbidden()

			if obj.state == InvoiceState.FINAL:
				if newstate != InvoiceState.VOID:
					return HttpResponseForbidden()
				return void_invoice( request, obj, data, *args, **kwargs )

			if newstate == InvoiceState.VOID:
				return delete_object( request, obj, data, *args, **kwargs )

			if newstate == InvoiceState.FINAL:
				return finalize_invoice( request, obj, data, *args, **kwargs )

			return HttpResponseServerError()

		return update_invoice( request, obj, data, *args, **kwargs )

