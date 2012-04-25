from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.contrib import messages

from common.views.modal import ModalLogic
from common.exceptions import *

from ..utils import OrgBusLog

from ..models import *
from ..forms import EditOrganization as EditOrganizationForm


class NewOrganization( ModalLogic ):

	def get_extra( self, request, dmap, obj, *args, **kwargs ):
		myobj = { 'form' : EditOrganizationForm() }
		return myobj

	def get_object( self, request, dmap, *args, **kwargs ):
		return None

	def perform( self, request, dmap, obj, extra, *args, **kwargs ):
		extra[ 'form' ] = EditOrganizationForm( dmap )
		if extra[ 'form' ].is_valid() is False:
			self.easy.make_get()
			return

		try:
			neworg = OrgBusLog.create( request.user, dmap )
		except BLE_Error, berror:
			messages.error( request, berror.message )
			self.easy.make_get()
			return

		messages.success( request, _('VMG_20005') % { 'url' : neworg.get_absolute_url(), 'name' : neworg.trading_name } )

		self.easy.notice();
		return neworg


class EditOrganization( ModalLogic ):

	def get_extra( self, request, dmap, obj, *args, **kwargs ):
		myobj = { 'form' : EditOrganizationForm( instance = obj ) }
		return myobj

	def get_object( self, request, dmap, *args, **kwargs ):
		return Organization.objects.get( refnum = dmap[ 'oid' ] )

	def perform( self, request, dmap, obj, extra, *args, **kwargs ):

		extra[ 'form' ] = EditOrganizationForm( dmap )
		if extra[ 'form' ].is_valid() is False:
			self.easy.make_get()
			return

		try:
			OrgBusLog.update( obj, dmap )
			obj.save()
		except BLE_Error, berror:
			messages.error( request, berror.message )
			self.easy.make_get()
			return


		messages.success( request, _('VMG_20005') % { 'url' : neworg.get_absolute_url(), 'name' : obj.trading_name } )

		self.easy.notice();
		return obj



