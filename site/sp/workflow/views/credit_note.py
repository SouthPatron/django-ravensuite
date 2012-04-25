from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from django.db.models import F,Q

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseServerError
from django.contrib import messages

from account.views import AccountPageView

from common.busobj.org import CreditNoteObj
from common.bushelp.org import CreditNoteHelper
from common.bushelp.org.actions import ActionFactory

from common.exceptions import *
from common.models import *


class CreditNoteList( AccountPageView ):
	template_name = 'pages/org/client/account/transaction/credit_note/index'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Client, refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = SourceDocument.objects.filter(
				Q( document_state = SourceDocumentState.FINAL ) | Q( document_state = SourceDocumentState.VOID ),
				client__refnum = self.url_kwargs.cid,
				client__organization__refnum = self.url_kwargs.oid,
				document_type = SourceDocumentType.CREDIT_NOTE
			)
		return obj_list

	def update_object( self, request, data, *args, **kwargs ):

		client = self.dataset[ 'instance' ]

		try:
			newo = CreditNoteObj()
			newo.initialize( client )
		except BLE_Error, berror:
			messages.error( request, berror.message )
			return redirect( client.get_credit_note_list_url() )

		return redirect( newo.get_absolute_url() )


class CreditNoteDraftList( AccountPageView ):
	template_name = 'pages/org/client/account/transaction/credit_note/draft-index'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Client, refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = SourceDocument.objects.filter( client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid, document_type = SourceDocumentType.CREDIT_NOTE, document_state = SourceDocumentState.DRAFT )
		return obj_list


class CreditNoteUnallocatedList( AccountPageView ):
	template_name = 'pages/org/client/account/transaction/credit_note/unallocated-index'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Client, refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = SourceDocument.objects.filter( client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid, document_type = SourceDocumentType.CREDIT_NOTE, document_state = SourceDocumentState.FINAL, total__gt = F('allocated') )
		return obj_list


class CreditNoteSingle( AccountPageView ):
	template_name = 'pages/org/client/account/transaction/credit_note/single'


	def get_object( self, request, *args, **kwargs ):
		obj = get_object_or_404( SourceDocument, refnum = self.url_kwargs.sdid, client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid )

		if obj.document_state == SourceDocumentState.DRAFT:
			self.template_name = 'pages/org/client/account/transaction/credit_note/single-draft'
		elif obj.document_state == SourceDocumentState.FINAL:
			self.template_name = 'pages/org/client/account/transaction/credit_note/single-final'
		elif obj.document_state == SourceDocumentState.VOID:
			self.template_name = 'pages/org/client/account/transaction/credit_note/single-void'

		return obj


	def update_object( self, request, data, *args, **kwargs ):

		obj = self.dataset[ 'instance' ]

		credit_note_data = {}

		credit_note_data[ 'state' ] = data.get( 'sd_state' )

		if credit_note_data[ 'state' ] is not None and long(credit_note_data['state']) == SourceDocumentState.DELETE:
			inv = CreditNoteObj()
			inv.wrap( obj )
			ActionFactory.instantiate( inv ).delete()
			messages.info( request, _('VMG_20003') )
			return redirect( obj.get_client().get_credit_note_list_url() )

		credit_note_data[ 'credit_note_date' ] = data.get( 'credit_note_date' )
		credit_note_data[ 'comment' ] = data.get( 'credit_note_comment', "" )
		credit_note_data[ 'items' ] = []
		
		for pos in range( len(data.getlist( 'description' )) ):
			credit_note_data[ 'items' ].append( [
						data.getlist( 'description' )[ pos ],
						data.getlist( 'units' )[ pos ],
						data.getlist( 'perunit' )[ pos ],
						data.getlist( 'tax_rate' )[ pos ]
					] )

		try:
			CreditNoteHelper.update( obj, credit_note_data )
		except BLE_Error, berror:
			messages.error( request, berror.message )
			return redirect( obj.get_absolute_url() )

		if obj.document_state == SourceDocumentState.DRAFT:
			return redirect( obj.get_client().get_draft_credit_note_list_url() )
	
		return redirect( obj.get_client().get_account_single_url() )

