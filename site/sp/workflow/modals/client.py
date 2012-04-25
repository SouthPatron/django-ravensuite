from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q,F


from common.views.modal import ModalLogic
from common.models import *

from common.buslog.org import ProjectBusLog
from common.busobj.org import SourceDocumentObj
from common.bushelp.org.allocator import Allocator
from common.exceptions import *

from common.utils.parse import *


class NewProject( ModalLogic ):

	def get_extra( self, request, dmap, obj, *args, **kwargs ):
		return None

	def get_object( self, request, dmap, *args, **kwargs ):
		return None

	def perform( self, request, dmap, obj, extra, *args, **kwargs ):
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

	def perform( self, request, dmap, obj, extra, *args, **kwargs ):

		invoice_refnum = dmap.get( 'refnum' )
		payment_amount = pnumparse( dmap.get( 'amount' ) )

		try:
			inv = SourceDocumentObj()
			inv.load( invoice_refnum )

			pay = SourceDocumentObj()
			pay.wrap( obj )

			alo = Allocator()
			alo.allocate( pay, inv, payment_amount )

		except BLE_Error, berror:
			messages.error( request, berror.message )
			self.easy.notice();
			return

		messages.success( request, _('VMG_21001') )
		self.easy.redirect();
		return pay.get_absolute_url();


class AccountTransactionAllocations( ModalLogic ):

	def get_extra( self, request, dmap, obj, *args, **kwargs ):
		sdo = SourceDocumentObj()
		sdo.wrap( obj )

		extra = {
			'allocations' : sdo.getAllocations(),
		}
		return extra

	def get_object( self, request, dmap, *args, **kwargs ):

		sd = get_object_or_404( SourceDocument,
				document_state = SourceDocumentState.FINAL,
				refnum = dmap[ 'sdid' ],
				client__refnum = dmap[ 'cid' ],
				client__organization__refnum = dmap[ 'oid' ]
			)

		return sd



class AccountTransactionDeallocate( ModalLogic ):

	def get_extra( self, request, dmap, obj, *args, **kwargs ):
		sdo = SourceDocumentObj()
		sdo.wrap( obj )
		alloc = sdo.getAllocations().get( dmap[ 'alocid' ] );
		extra = { 'allocation' : alloc }
		return extra


	def get_object( self, request, dmap, *args, **kwargs ):
		sd = get_object_or_404( SourceDocument,
				document_state = SourceDocumentState.FINAL,
				refnum = dmap[ 'sdid' ],
				client__refnum = dmap[ 'cid' ],
				client__organization__refnum = dmap[ 'oid' ]
			)

		return sd



	def perform( self, request, dmap, obj, extra, *args, **kwargs ):

		alo = Allocator()

		sdo = SourceDocumentObj()
		sdo.wrap( obj )

		try:
			alo.deallocate( sdo, extra[ 'allocation' ].id )

		except BLE_Error, berror:
			messages.error( request, berror.message )
			self.easy.notice();
			return

		messages.success( request, _('VMG_21001') )
		self.easy.redirect();
		return obj.get_absolute_url();

