from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q,F


from common.views.modal import ModalLogic
from common.models import *

from common.buslog.org import ProjectBusLog
from common.busobj.org import SourceDocumentObj
from common.exceptions import *


class NewProject( ModalLogic ):

	def get_extra( self, request, dmap, obj, *args, **kwargs ):
		return None

	def get_object( self, request, dmap, *args, **kwargs ):
		return None

	def perform( self, request, dmap, obj, extra, fmt, *args, **kwargs ):
		try:
			client = Client.objects.get( refnum = dmap[ 'cid' ], organization__refnum = dmap[ 'oid' ] )

			newo = ProjectBusLog.create(
						client,
						dmap[ 'status' ],
						dmap[ 'name' ],
						dmap[ 'description'],
					)
		except BLE_Error, berror:
			messages.error( request, berror.message )
			self.easy.notice();
			return

		self.easy.redirect();
		return newo.get_absolute_url();


class AccountTransactionAllocate( ModalLogic ):

	def get_extra( self, request, dmap, obj, *args, **kwargs ):
		
		sdo = SourceDocumentObj()
		sdo.wrap( obj )

		extra = {
			'available' : sdo.getTotals().getUnallocated(),

			'outstanding' : {
				'invoices' : SourceDocument.objects.filter(
						document_type = SourceDocumentType.INVOICE,
						document_state = SourceDocumentState.FINAL,
						total__gt = F( 'allocated' ),
						client__refnum = dmap[ 'cid' ],
						client__organization__refnum = dmap[ 'oid' ]
					),

				'refunds' : SourceDocument.objects.filter(
						document_type = SourceDocumentType.REFUND,
						document_state = SourceDocumentState.FINAL,
						total__gt = F( 'allocated' ),
						client__refnum = dmap[ 'cid' ],
						client__organization__refnum = dmap[ 'oid' ]
					),
			}
		}
		return extra

	def get_object( self, request, dmap, *args, **kwargs ):

		sd = get_object_or_404( SourceDocument,

				Q( document_type = SourceDocumentType.PAYMENT ) |
					Q( document_type = SourceDocumentType.CREDIT_NOTE ),
				document_state = SourceDocumentState.FINAL,
				total__gt = F( 'allocated' ),

				refnum = dmap[ 'sdid' ],
				client__refnum = dmap[ 'cid' ],
				client__organization__refnum = dmap[ 'oid' ]
			)

		return sd

	def perform( self, request, dmap, obj, extra, fmt, *args, **kwargs ):
		return pmt.get_absolute_url();




