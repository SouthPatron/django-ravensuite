from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from django.db.models import F,Q

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from common.views.component import ComponentView
from common.busobj.org import SourceDocumentObj
from common.bushelp.org.allocator import Allocator
from common.utils.parse import *
from common.exceptions import *
from common.models import *


# ----------------------------------------------------------------

class RefundComponents( ComponentView ):
	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404(
					SourceDocument,
					refnum = self.url_kwargs.sdid,
					client__refnum = self.url_kwargs.cid,
					client__organization__refnum = self.url_kwargs.oid
				)


class PcAllocateRefund( RefundComponents ):
	template_name = 'modals/org/refund/allocate'

	def post_html( self, request, obj, data, *args, **kwargs ):

		refnum = data.get( "refnum" )
		amount = pnumparse( data.get( "amount" ) )

		try:

			inv = SourceDocumentObj()
			inv.load( refnum )

			ref = SourceDocumentObj()
			ref.wrap( obj )

			alo = Allocator()
			alo.allocate( inv, ref, amount )

		except BLE_Error, berror:
			messages.error( request, berror.message )
			return redirect( obj.get_single_url() )

		messages.success( request, _('VMG_21003') )
		return redirect( obj.get_single_url() )




