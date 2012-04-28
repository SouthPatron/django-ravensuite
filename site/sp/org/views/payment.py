from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from django.db.models import F,Q

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseServerError
from django.contrib import messages

from common.views.pageview import PageView

from common.busobj.org import PaymentObj, SourceDocumentObj, RefundObj

from common.bushelp.org.actions import ActionFactory

from common.utils.parse import *

from common.exceptions import *
from common.models import *


class PaymentList( PageView ):
	template_name = 'pages/org/client/account/transaction/payment/index'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Client, refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = SourceDocument.objects.filter(
				Q( document_state = SourceDocumentState.FINAL ) | Q( document_state = SourceDocumentState.VOID ),
				client__refnum = self.url_kwargs.cid,
				client__organization__refnum = self.url_kwargs.oid,
				document_type = SourceDocumentType.PAYMENT
			)
		return obj_list

	
	def update_object( self, request, data, *args, **kwargs ):

		client = self.dataset[ 'instance' ]

		try:
			newo = PaymentObj()
			newo.initialize( client )
		except BLE_Error, berror:
			messages.error( request, berror.message )
			return redirect( client.get_account_single_url() )

		return redirect( newo.get_absolute_url() )


class PaymentDraftList( PageView ):
	template_name = 'pages/org/client/account/transaction/payment/draft-index'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Client, refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = SourceDocument.objects.filter( client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid, document_type = SourceDocumentType.PAYMENT, document_state = SourceDocumentState.DRAFT )
		return obj_list


class PaymentUnallocatedList( PageView ):
	template_name = 'pages/org/client/account/transaction/payment/unallocated-index'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Client, refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = SourceDocument.objects.filter( client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid, document_type = SourceDocumentType.PAYMENT, document_state = SourceDocumentState.FINAL, total__gt = F('allocated') )
		return obj_list




class PaymentSingle( PageView ):
	template_name = 'pages/org/client/account/transaction/payment/single'

	def get_object( self, request, *args, **kwargs ):
		obj = get_object_or_404( SourceDocument, refnum = self.url_kwargs.sdid, client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid )

		if obj.document_state == SourceDocumentState.DRAFT:
			self.template_name = 'pages/org/client/account/transaction/payment/single-draft'
		elif obj.document_state == SourceDocumentState.FINAL:
			self.template_name = 'pages/org/client/account/transaction/payment/single-final'
		elif obj.document_state == SourceDocumentState.VOID:
			self.template_name = 'pages/org/client/account/transaction/payment/single-void'

		return obj



	def update_object( self, request, data, *args, **kwargs ):

		obj = self.dataset[ 'instance' ]

		state = long( data.get( 'sd_state', obj.document_state ) )

		if state == SourceDocumentState.DELETE:
			pmt = PaymentObj()
			pmt.wrap( obj )
			ActionFactory.instantiate( pmt ).delete()
			messages.info( request, _('VMG_20006') )
			return redirect( obj.get_client().get_draft_payment_list_url() )


		pmt = PaymentObj()
		pmt.wrap( obj )

		amount = pmt.getTotals().getTotal()
		payment_date = pmt.getSpecs().getPaymentDate()
		comment = pmt.getSpecs().getComment()


		if state == SourceDocumentState.DRAFT:
			amount = data.get( 'amount', None )

			if amount is not None:
				amount = pnumparse( amount )
				pmt.getLines().clear()
				pmt.getLines().add(
					'Payment Received',
					100,
					amount,
					TaxRate.NONE
				)

			payment_date = data.get( 'payment_date', None )
			if payment_date is not None:
				pmt.getSpecs().setPaymentDate( pdateparse( payment_date ) )

		comment = data.get( 'payment_comment', None )
		if comment is not None:
			pmt.getSpecs().setComment( comment )

		if state != obj.document_state:

			acf = ActionFactory.instantiate( pmt )

			if state == SourceDocumentState.FINAL:
				acf.finalize()

			if state == SourceDocumentState.VOID:
				acf.void()

		return redirect( pmt.get_absolute_url() )



