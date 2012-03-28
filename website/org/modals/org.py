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

from ..forms.client import AddClient


class NewOrganization( ModalLogic ):

	def get_extra( self, request, dmap, *args, **kwargs ):
		return None

	def get_object( self, request, dmap, *args, **kwargs ):
		return None

	def perform( self, request, dmap, obj, extra, fmt, *args, **kwargs ):
		try:
			neworg = OrgBusLog.create( request.user, dmap[ 'trading_name' ] )
			UserBusLog.grant( request.user, neworg, UserCategory.OWNER )
		except BLE_Error, berror:
			messages.error( request, berror.message )
			self.easy.make_get()
			return

		messages.success( request, _('VMG_20005') % { 'url' : neworg.get_single_url(), 'name' : neworg.trading_name } )

		self.easy.notice();
		return neworg


class NewClient( ModalLogic ):

	def get_extra( self, request, dmap, *args, **kwargs ):
		myobj = { 'form' : AddClient() }
		return myobj

	def get_object( self, request, dmap, *args, **kwargs ):
		return None

	def perform( self, request, dmap, obj, extra, fmt, *args, **kwargs ):

		org = Organization.objects.get( refnum = dmap[ 'oid' ] )

		extra[ 'form' ] = AddClient( dmap )
		if extra[ 'form' ].is_valid() is False:
			self.easy.make_get()
			return

		try:
			newo = ClientBusLog.create( org, dmap )
		except BLE_Error, berror:
			messages.error( request, berror.message )
			self.easy.make_get()
			return

		messages.success( request, _('VMG_20002') % { 'url' : newo.get_single_url(), 'name' : newo.trading_name } )

		self.easy.notice();
		return newo


