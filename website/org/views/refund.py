from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseServerError
from django.contrib import messages

from common.views.singleobjectview import SingleObjectView
from common.views.listview import ListView

from common.buslog.org import RefundBusLog

from common.exceptions import *
from common.models import *


class RefundList( ListView ):
	template_name = 'pages/org/refund/index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = Refund.objects.filter( client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid )
		return obj_list

	def _create_object( self, request, data, *args, **kwargs ):
		client = Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )
		newo = RefundBusLog.create( client, data )
		return newo
		
	
	def create_object_html( self, request, data, *args, **kwargs ):
		client = Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

		try:
			newo = self._create_object( request, data, *args, **kwargs )
		except BusLogError, berror:
			messages.error( request, berror.message )
			return redirect( client.get_account_single_url() )

		return redirect( newo.get_single_url() )


	def create_object_json( self, request, data, *args, **kwargs ):
		newo = self._create_object( request, data, *args, **kwargs )
		resp = { 'url' : newo.get_single_url() }
		return self.api_resp( resp )


class RefundSingle( SingleObjectView ):
	template_name = 'pages/org/refund/single'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Refund, refnum = self.url_kwargs.refid, client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid )



