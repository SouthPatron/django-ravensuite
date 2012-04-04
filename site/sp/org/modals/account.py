from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from django.shortcuts import redirect
from django.contrib import messages

from common.views.modal import ModalLogic
from common.models import *

from common.busobj.org import InvoiceObj, PaymentObj, CreditNoteObj, RefundObj
from common.exceptions import *


class AccountNewInvoice( ModalLogic ):

	def get_extra( self, request, dmap, obj, *args, **kwargs ):
		return None

	def get_object( self, request, dmap, *args, **kwargs ):
		return None

	def perform( self, request, dmap, obj, extra, fmt, *args, **kwargs ):
		try:
			client = Client.objects.get( refnum = dmap[ 'cid' ], organization__refnum = dmap[ 'oid' ] )

			inv = InvoiceObj()
			inv.initialize( client )

		except BLE_Error, berror:
			messages.error( request, berror.message )
			self.easy.notice();
			return

		self.easy.redirect();
		return inv.get_single_url();


class AccountNewPayment( ModalLogic ):

	def get_extra( self, request, dmap, obj, *args, **kwargs ):
		return None

	def get_object( self, request, dmap, *args, **kwargs ):
		return None

	def perform( self, request, dmap, obj, extra, fmt, *args, **kwargs ):
		try:
			client = Client.objects.get( refnum = dmap[ 'cid' ], organization__refnum = dmap[ 'oid' ] )

			pmt = PaymentObj()
			pmt.initialize( client )

		except BLE_Error, berror:
			messages.error( request, berror.message )
			self.easy.notice();
			return

		self.easy.redirect();
		return pmt.get_single_url();


class AccountNewCreditnote( ModalLogic ):

	def get_extra( self, request, dmap, obj, *args, **kwargs ):
		return None

	def get_object( self, request, dmap, *args, **kwargs ):
		return None

	def perform( self, request, dmap, obj, extra, fmt, *args, **kwargs ):
		try:
			client = Client.objects.get( refnum = dmap[ 'cid' ], organization__refnum = dmap[ 'oid' ] )

			pmt = CreditNoteObj()
			pmt.initialize( client )

		except BLE_Error, berror:
			messages.error( request, berror.message )
			self.easy.notice();
			return

		self.easy.redirect();
		return pmt.get_single_url();


class AccountNewRefund( ModalLogic ):

	def get_extra( self, request, dmap, obj, *args, **kwargs ):
		return None

	def get_object( self, request, dmap, *args, **kwargs ):
		return None

	def perform( self, request, dmap, obj, extra, fmt, *args, **kwargs ):
		try:
			client = Client.objects.get( refnum = dmap[ 'cid' ], organization__refnum = dmap[ 'oid' ] )

			pmt = RefundObj()
			pmt.initialize( client )

		except BLE_Error, berror:
			messages.error( request, berror.message )
			self.easy.notice();
			return

		self.easy.redirect();
		return pmt.get_single_url();



