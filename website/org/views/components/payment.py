from __future__ import unicode_literals

from django.db.models import F,Q

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from common.busobj.org import PaymentObj, SourceDocumentObj, RefundObj
from common.views.component import ComponentView

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
	template_name = 'components/org/payment/allocate_payment'

	def post_html( self, request, obj, data, *args, **kwargs ):

		invoice_refnum = data.get( "invoice-refnum" )
		payment_amount = pnumparse( data.get( "payment-amount" ) )

		try:

			inv = SourceDocumentObj()
			inv.load( invoice_refnum )

			pay = SourceDocumentObj()
			pay.wrap( obj )

			pay.getAllocations().allocate( inv, payment_amount )

		except BusLogError, berror:
			messages.error( request, berror.message )
			return redirect( obj.get_single_url() )

		messages.success( request, 'Successfully allocated.' )
		return redirect( obj.get_single_url() )


class PcDeallocatePayment( PaymentComponents ):
	template_name = 'components/org/payment/deallocate_payment'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404(
					SourceDocumentAllocation,
					id = self.url_kwargs.alocid,
					source__refnum = self.url_kwargs.sdid,
					source__client__refnum = self.url_kwargs.cid,
					source__client__organization__refnum = self.url_kwargs.oid
				)



	def post_html( self, request, obj, data, *args, **kwargs ):

		try:
			pay = SourceDocumentObj()
			pay.wrap( obj.source )
			pay.getAllocations().clear_one( obj )

		except BusLogError, berror:
			messages.error( request, berror.message )
			return redirect( obj.source.get_single_url() )

		messages.success( request, 'Successfully deallocated.' )
		return redirect( obj.source.get_single_url() )


class PcRefundPayment( PaymentComponents ):
	template_name = 'components/org/payment/refund'

	def post_html( self, request, obj, data, *args, **kwargs ):

		refund_amount = pnumparse( data.get( "refund-amount" ) )
		refund_date = pdateparse( data.get( "refund-date" ) )

		try:

			pay = SourceDocumentObj()
			pay.wrap( obj )

			ref = RefundObj()
			ref.initialize( pay, refund_amount, refund_date )
			ref.getSpecs().setComment( "" )

		except BusLogError, berror:
			messages.error( request, berror.message )
			return redirect( obj.get_single_url() )

		messages.success( request, 'Successfully allocated.' )
		return redirect( obj.get_single_url() )



