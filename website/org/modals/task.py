from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.contrib import messages

from common.views.modal import ModalLogic
from common.models import *
from common.buslog.org import TaskBusLog
from common.exceptions import *


class ActivityNewTask( ModalLogic ):

	def get_extra( self, request, dmap, obj, *args, **kwargs ):
		return None

	def get_object( self, request, dmap, *args, **kwargs ):
		return None

	def perform( self, request, dmap, obj, extra, fmt, *args, **kwargs ):
		try:

			newtask = TaskBusLog.create( 
						Activity.objects.get( id = dmap[ 'actid' ], organization__refnum = dmap[ 'oid' ] ),
						dmap[ 'name' ],
						dmap[ 'description' ],
					)

		except BLE_Error, berror:
			messages.error( request, berror.message )
			self.easy.notice();
			return

		self.easy.redirect();
		return newtask.get_single_url();


