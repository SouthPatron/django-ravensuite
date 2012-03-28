from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from django.shortcuts import redirect
from django.contrib import messages

from common.views.modal import ModalLogic
from common.models import *

from common.buslog.org import ProjectBusLog
from common.exceptions import *


class ClientNewProject( ModalLogic ):

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
		return newo.get_single_url();



