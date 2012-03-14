from __future__ import unicode_literals

from django.utils.translation import ugettext as _


from django.db.models import F,Q

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from common.views.component import ComponentView

from common.busobj.org import PaymentObj, SourceDocumentObj
from common.busobj.org.factory import Factory
from common.bushelp.org.allocator import Allocator
from common.bushelp.org.actions import ActionFactory

from common.utils.parse import *

from common.exceptions import *
from common.models import *


# ----------------------------------------------------------------

class PaymentComponents( ComponentView ):
	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404(
					SourceDocument,
					refnum = self.url_kwargs.sdid,
					client__refnum = self.url_kwargs.cid,
					client__organization__refnum = self.url_kwargs.oid
				)


class PcAllocatePayment( PaymentComponents ):
	template_name = 'modals/org/payment/allocate'

	def post_html( self, request, obj, data, *args, **kwargs ):

		invoice_refnum = data.get( "invoice-refnum" )
		payment_amount = pnumparse( data.get( "payment-amount" ) )

		try:

			inv = SourceDocumentObj()
			inv.load( invoice_refnum )

			pay = SourceDocumentObj()
			pay.wrap( obj )

			alo = Allocator()
			alo.allocate( pay, inv, payment_amount )

		except BLE_Error, berror:
			messages.error( request, berror.message )
			return redirect( obj.get_single_url() )

		messages.success( request, _('VMG_21001') )
		return redirect( obj.get_single_url() )


class PcDeallocatePayment( PaymentComponents ):
	template_name = 'modals/org/payment/deallocate'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404(
					SourceDocumentAllocation,
					id = self.url_kwargs.alocid,
					source__refnum = self.url_kwargs.sdid,
					source__client__refnum = self.url_kwargs.cid,
					source__client__organization__refnum = self.url_kwargs.oid
				)


	def post_html( self, request, obj, extra, data, *args, **kwargs ):

		try:
			pay = Factory.instantiate( obj.source )

			alo = Allocator()
			alo.deallocate( pay, obj.id )


		except BLE_Error, berror:
			messages.error( request, berror.message )
			return redirect( obj.source.get_single_url() )

		messages.success( request, _('VMG_21002') )
		return redirect( obj.source.get_single_url() )


class PcRefundPayment( PaymentComponents ):
	template_name = 'modals/org/payment/refund'

	def post_html( self, request, obj, data, *args, **kwargs ):

		refund_amount = pnumparse( data.get( "refund-amount" ) )
		refund_date = pdateparse( data.get( "refund-date" ) )

		try:
			pay = Factory.instantiate( obj )
			pay.wrap( obj )

#			ref = RefundHelper.create( pay, refund_amount, refund_date )
#			ref.getSpecs().setComment( "" )

		except BLE_Error, berror:
			messages.error( request, berror.message )
			return redirect( obj.get_single_url() )

		messages.success( request, _('NIL') )
		return redirect( obj.get_single_url() )



