from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from django.db.models import F,Q

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseServerError
from django.contrib import messages

from common.views.pageview import PageView

from common.busobj.org import InvoiceObj
from common.bushelp.org import InvoiceHelper

from common.bushelp.org.actions import ActionFactory

from common.exceptions import *
from common.models import *


class InvoiceList( PageView ):
	template_name = 'pages/org/client/account/transaction/invoice/index'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Client, refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = SourceDocument.objects.filter(
				Q( document_state = SourceDocumentState.FINAL ) | Q( document_state = SourceDocumentState.VOID ),
				client__refnum = self.url_kwargs.cid,
				client__organization__refnum = self.url_kwargs.oid,
				document_type = SourceDocumentType.INVOICE
			)
		return obj_list

	
	def update_object( self, request, data, *args, **kwargs ):

		client = self.dataset[ 'instance' ]

		try:
			newo = InvoiceObj()
			newo.initialize( client )
		except BLE_Error, berror:
			messages.error( request, berror.message )
			return redirect( client.get_invoice_list_url() )

		return redirect( newo.get_absolute_url() )



class InvoiceDraftList( PageView ):
	template_name = 'pages/org/client/account/transaction/invoice/draft-index'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Client, refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = SourceDocument.objects.filter( client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid, document_type = SourceDocumentType.INVOICE, document_state = SourceDocumentState.DRAFT )
		return obj_list


class InvoiceUnpaidList( PageView ):
	template_name = 'pages/org/client/account/transaction/invoice/unpaid-index'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Client, refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = SourceDocument.objects.filter( client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid, document_type = SourceDocumentType.INVOICE, document_state = SourceDocumentState.FINAL, total__gt = F('allocated') )
		return obj_list



class InvoiceSingle( PageView ):
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



	def update_object( self, request, data, *args, **kwargs ):

		obj = self.dataset[ 'instance' ]

		invoice_data = {}

		invoice_data[ 'state' ] = data.get( 'sd_state' )

		if invoice_data[ 'state' ] is not None and long(invoice_data['state']) == SourceDocumentState.DELETE:
			inv = InvoiceObj()
			inv.wrap( obj )
			ActionFactory.instantiate( inv ).delete()
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
			return redirect( obj.get_absolute_url() )

		if obj.document_state == SourceDocumentState.DRAFT:
			return redirect( obj.get_client().get_draft_invoice_list_url() )
	
		return redirect( obj.get_client().get_account_single_url() )



