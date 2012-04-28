from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response, redirect
from django.contrib import messages

from django.core.urlresolvers import reverse

from common.views.modal import ModalLogic
from common.models import *

from common.buslog.org.client import *
from common.buslog.org.org import *
from common.buslog.org.user import *
from common.exceptions import *

from ..forms.client import EditContact as EditContactForm



class NewContact( ModalLogic ):

	def get_extra( self, request, dmap, obj, *args, **kwargs ):
		myobj = { 'form' : EditContactForm() }
		return myobj


	def perform( self, request, dmap, obj, extra, *args, **kwargs ):

		org = Organization.objects.get( refnum = dmap[ 'oid' ] )

		extra[ 'form' ] = EditContactForm( dmap )
		if extra[ 'form' ].is_valid() is False:
			self.easy.make_get()
			return

		try:
			newo = ContactBusLog.create( org, dmap )
		except BLE_Error, berror:
			messages.error( request, berror.message )
			self.easy.make_get()
			return

		messages.success( request, _('VMG_20002') % { 'url' : newo.get_absolute_url(), 'name' : newo.trading_name } )

		self.easy.notice()

		self.additional = {
			'buttons' : (
					{ 'label' : _('VMG_20002_BUTTON_0001'), 'url' : org.get_client_list_url() },
					{ 'label' : _('VMG_20002_BUTTON_0002'), 'url' : newo.get_absolute_url() },
				)
		}

		return newo


class EditContact( ModalLogic ):

	def get_extra( self, request, dmap, obj, *args, **kwargs ):
		myobj = { 'form' : EditContactForm( instance = obj ) }
		return myobj

	def get_object( self, request, dmap, *args, **kwargs ):
		return Contact.objects.get( refnum = dmap[ 'cid' ], organization__refnum = dmap[ 'oid' ] )

	def perform( self, request, dmap, obj, extra, *args, **kwargs ):

		extra[ 'form' ] = EditContactForm( dmap )
		if extra[ 'form' ].is_valid() is False:
			self.easy.make_get()
			return

		try:
			ContactBusLog.update( obj, dmap )
			obj.save()
		except BLE_Error, berror:
			messages.error( request, berror.message )
			self.easy.make_get()
			return

		messages.success( request, _('VMG_20002') % { 'url' : obj.get_absolute_url(), 'name' : obj.trading_name } )

		self.easy.notice();
		return obj



