from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from django.db.models import F,Q

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseServerError
from django.contrib import messages

from common.views.singleobjectview import SingleObjectView
from common.views.listview import ListView

from common.busobj.org import InvoiceObj
from common.bushelp.org import InvoiceHelper

from common.bushelp.org.actions import ActionFactory

from common.exceptions import *
from common.models import *


class InvoiceList( ListView ):
	template_name = 'pages/org/client/account/transaction/invoice/index'

	def get_object( self, request, obj_list, fmt, *args, **kwargs ):
		return Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = SourceDocument.objects.filter(
				Q( document_state = SourceDocumentState.FINAL ) | Q( document_state = SourceDocumentState.VOID ),
				client__refnum = self.url_kwargs.cid,
				client__organization__refnum = self.url_kwargs.oid,
				document_type = SourceDocumentType.INVOICE
			)
		return obj_list

	def _create_object( self, request, data, *args, **kwargs ):
		client = Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

		inv = InvoiceObj()
		inv.initialize( client )
		return inv
		
	
	def create_object_html( self, request, data, *args, **kwargs ):

		try:
			newo = self._create_object( request, data, *args, **kwargs )
		except BLE_Error, berror:
			messages.error( request, berror.message )
			client = Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )
			return redirect( client.get_invoice_list_url() )
		except Exception, error:
			print error

		return redirect( newo.get_single_url() )


	def create_object_json( self, request, data, *args, **kwargs ):
		newo = self._create_object( request, data, *args, **kwargs )
		resp = { 'url' : newo.get_single_url() }
		return self.api_resp( resp )


class InvoiceDraftList( ListView ):
	template_name = 'pages/org/client/account/transaction/invoice/draft-index'

	def get_object( self, request, obj_list, fmt, *args, **kwargs ):
		return Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = SourceDocument.objects.filter( client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid, document_type = SourceDocumentType.INVOICE, document_state = SourceDocumentState.DRAFT )
		return obj_list


class InvoiceUnpaidList( ListView ):
	template_name = 'pages/org/client/account/transaction/invoice/unpaid-index'

	def get_object( self, request, obj_list, fmt, *args, **kwargs ):
		return Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = SourceDocument.objects.filter( client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid, document_type = SourceDocumentType.INVOICE, document_state = SourceDocumentState.FINAL, total__gt = F('allocated') )
		return obj_list



class InvoiceSingle( SingleObjectView ):
	template_name = 'pages/org/client/account/transaction/invoice/single'


	def get_object( self, request, *args, **kwargs ):
		obj = get_object_or_404( SourceDocument, refnum = self.url_kwargs.sdid, client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid )

		if obj.document_state == SourceDocumentState.DRAFT:
			self.template_name = 'pages/org/client/account/transaction/invoice/single-draft'
		elif obj.document_state == SourceDocumentState.FINAL:
			self.template_name = 'pages/org/client/account/transaction/invoice/single-final'
		elif obj.document_state == SourceDocumentState.VOID:
			self.template_name = 'pages/org/client/account/transaction/invoice/single-void'

		return obj

	def delete_object( self, request, ob, *args, **kwargs ):
		inv = InvoiceObj()
		inv.wrap( ob )
		ActionFactory.instantiate( inv ).delete()
		return redirect( ob.get_client().get_invoice_list_url() )


	def update_object_html( self, request, obj, data, *args, **kwargs ):

		invoice_data = {}

		invoice_data[ 'state' ] = data.get( 'invoice_state' )

		if invoice_data[ 'state' ] is not None and long(invoice_data['state']) == SourceDocumentState.DELETE:
			rc = self.delete_object( request, obj, *args, **kwargs )
			messages.info( request, _('VMG_20004') )
			return redirect( obj.get_client().get_draft_invoice_list_url() )

		invoice_data[ 'invoice_date' ] = data.get( 'invoice_date' )
		invoice_data[ 'due_date' ] = data.get( 'due_date' )
		invoice_data[ 'comment' ] = data.get( 'invoice_comment', "" )
		invoice_data[ 'items' ] = []
		
		for pos in range( len(data.getlist( 'description' )) ):
			invoice_data[ 'items' ].append( [
						data.getlist( 'description' )[ pos ],
						data.getlist( 'units' )[ pos ],
						data.getlist( 'perunit' )[ pos ],
						data.getlist( 'tax_rate' )[ pos ]
					] )

		try:
			InvoiceHelper.update( obj, invoice_data )
		except BLE_Error, berror:
			messages.error( request, berror.message )
			return redirect( obj.get_single_url() )

		if obj.document_state == SourceDocumentState.DRAFT:
			return redirect( obj.get_client().get_draft_invoice_list_url() )
	
		return redirect( obj.get_client().get_account_single_url() )





