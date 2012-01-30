from __future__ import unicode_literals

from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseServerError
from django.contrib import messages

from common.views.singleobjectview import SingleObjectView
from common.views.listview import ListView

from common.buslog.org import RefundBusLog
from common.busobj.org import RefundObj

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


class RefundSingle( SingleObjectView ):
	template_name = 'pages/org/refund/single'

	def get_object( self, request, *args, **kwargs ):

		obj = get_object_or_404(
			SourceDocument,
			refnum = self.url_kwargs.sdid,
			client__refnum = self.url_kwargs.cid,
			client__organization__refnum = self.url_kwargs.oid
		)

		if obj.document_state == SourceDocumentState.FINAL:
			self.template_name = 'pages/org/refund/single-final'
		elif obj.document_state == SourceDocumentState.VOID:
			self.template_name = 'pages/org/refund/single-void'

		return obj



	def update_object_html( self, request, obj, data, *args, **kwargs ):

		state = long( data.get( 'refund_state', obj.document_state ) )

		mobj = RefundObj()
		mobj.wrap( obj )

		comment = mobj.getSpecs().getComment()

		comment = data.get( 'refund_comment', None )
		if comment is not None:
			mobj.getSpecs().setComment( comment )

		if state != obj.document_state:

			if state == SourceDocumentState.VOID:
				mobj.getActions().void()


		return redirect( mobj.get_single_url() )



