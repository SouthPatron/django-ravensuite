from __future__ import unicode_literals

from django.db.models import F,Q

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseServerError
from django.contrib import messages

from common.views.singleobjectview import SingleObjectView
from common.views.listview import ListView

from common.busobj.org import RefundObj, SourceDocumentObj

from common.bushelp.org.actions import ActionFactory

from common.utils.parse import *

from common.exceptions import *
from common.models import *


class RefundList( ListView ):
	template_name = 'pages/org/refund/index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = SourceDocument.objects.filter(
				Q( document_state = SourceDocumentState.FINAL ) | Q( document_state = SourceDocumentState.VOID ),
				client__refnum = self.url_kwargs.cid,
				client__organization__refnum = self.url_kwargs.oid,
				document_type = SourceDocumentType.REFUND
			)
		return obj_list

	def _create_object( self, request, *args, **kwargs ):
		client = Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

		pmt = RefundObj()
		pmt.initialize( client )
		return pmt


	def create_object_html( self, request, data, *args, **kwargs ):

		try:
			newo = self._create_object( request, *args, **kwargs )
		except BusLogError, berror:
			messages.error( request, berror.message )
			client = Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )
			return redirect( client.get_account_single_url() )

		return redirect( newo.get_single_url() )


	def create_object_json( self, request, data, *args, **kwargs ):
		newo = self._create_object( request, *args, **kwargs )
		resp = { 'url' : newo.get_single_url() }
		return self.api_resp( resp )


class RefundDraftList( ListView ):
	template_name = 'pages/org/refund/draft-index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = SourceDocument.objects.filter( client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid, document_type = SourceDocumentType.REFUND, document_state = SourceDocumentState.DRAFT )
		return obj_list


class RefundUnallocatedList( RefundList ):
	template_name = 'pages/org/refund/unallocated-index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = SourceDocument.objects.filter( client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid, document_type = SourceDocumentType.REFUND, document_state = SourceDocumentState.FINAL, total__gt = F('allocated') )
		return obj_list





class RefundSingle( SingleObjectView ):
	template_name = 'pages/org/refund/single'


	def get_object( self, request, *args, **kwargs ):
		obj = get_object_or_404( SourceDocument, refnum = self.url_kwargs.sdid, client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid )

		if obj.document_state == SourceDocumentState.DRAFT:
			self.template_name = 'pages/org/refund/single-draft'
		elif obj.document_state == SourceDocumentState.FINAL:
			self.template_name = 'pages/org/refund/single-final'
		elif obj.document_state == SourceDocumentState.VOID:
			self.template_name = 'pages/org/refund/single-void'

		return obj

	def delete_object( self, request, ob, *args, **kwargs ):
		pmt = RefundObj()
		pmt.wrap( ob )
		ActionFactory.instantiate( pmt ).delete()
		return redirect( ob.get_client().get_draft_refund_list_url() )


	def update_object_html( self, request, obj, data, *args, **kwargs ):

		state = long( data.get( 'refund_state', obj.document_state ) )

		if state == SourceDocumentState.DELETE:
			rc = self.delete_object( request, obj, *args, **kwargs )
			messages.info( request, 'The draft refund has been deleted' )
			return rc


		pmt = RefundObj()
		pmt.wrap( obj )

		amount = pmt.getTotals().getTotal()
		refund_date = pmt.getSpecs().getRefundDate()
		comment = pmt.getSpecs().getComment()


		if state == SourceDocumentState.DRAFT:
			amount = data.get( 'amount', None )

			if amount is not None:
				amount = pnumparse( amount )
				pmt.getLines().clear()
				pmt.getLines().add(
					'Refund Received',
					100,
					amount,
					TaxRate.NONE
				)

			refund_date = data.get( 'refund_date', None )
			if refund_date is not None:
				pmt.getSpecs().setRefundDate( pdateparse( refund_date ) )

		comment = data.get( 'refund_comment', None )
		if comment is not None:
			pmt.getSpecs().setComment( comment )

		if state != obj.document_state:

			acf = ActionFactory.instantiate( pmt )

			if state == SourceDocumentState.FINAL:
				acf.finalize()

			if state == SourceDocumentState.VOID:
				acf.void()

		return redirect( pmt.get_single_url() )





