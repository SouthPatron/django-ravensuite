from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response, redirect
from django.contrib import messages

from django.core.urlresolvers import reverse

from common.views.modal import ModalLogic
from common.models import *

from common.buslog.org.org import *
from common.buslog.org.user import *
from common.exceptions import *


class NewOrganization( ModalLogic ):

	def prepare( self, *args, **kwargs ):
		pass

	def get_extra( self, request, dmap, *args, **kwargs ):
		return None

	def get_object( self, request, dmap, *args, **kwargs ):
		return {}

	def perform( self, request, dmap, obj, extra, fmt, *args, **kwargs ):

		messages.success( request, 'We rule the world!' )
		self.easy.make_get()
		return

		try:
			neworg = OrgBusLog.create( request.user, dmap[ 'trading_name' ] )
			UserBusLog.grant( request.user, neworg, UserCategory.OWNER )
		except BLE_Error, berror:
			messages.error( request, berror.message )
			self.easy.make_get()
			return

		messages.success( request, _('VMG_20005') % { 'url' : neworg.get_single_url(), 'name' : neworg.trading_name } )
		return neworg


