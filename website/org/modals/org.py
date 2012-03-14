from __future__ import unicode_literals

from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response, redirect

from common.views.modal import ModalLogic
from common.models import *


class NewOrganization( ModalLogic ):

	def get_extra( self, request, dmap, *args, **kwargs ):
		return None

	def get_object( self, request, dmap, *args, **kwargs ):
		obj = Organization.objects.get( id = dmap[ 'oid' ] )
		return obj

	def perform( self, request, dmap, obj, extra, fmt, *args, **kwargs ):
		return None



