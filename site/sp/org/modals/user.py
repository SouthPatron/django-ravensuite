from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.contrib import messages

from common.views.modal import ModalLogic
from common.models import *
from common.buslog.org import UserBusLog
from common.exceptions import *


class NewUser( ModalLogic ):

	def get_extra( self, request, dmap, obj, *args, **kwargs ):
		return None

	def get_object( self, request, dmap, *args, **kwargs ):
		return None

	def perform( self, request, dmap, obj, extra, fmt, *args, **kwargs ):
		try:
			newgrant = UserBusLog.invite_user( 
							dmap[ 'first_name' ],
							dmap[ 'last_name' ],
							dmap[ 'email_address' ],
							Organization.objects.get( refnum = dmap[ 'oid' ] ),
							dmap[ 'category' ]
						)

		except BLE_Error, berror:
			messages.error( request, berror.message )
			self.easy.notice();
			return

		self.easy.redirect();
		return newgrant.get_absolute_url();


