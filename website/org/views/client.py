from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from common.views.singleobjectview import SingleObjectView
from common.views.listview import ListView

from common.models import *
from common.buslog.org.client import ClientBusLog
from common.exceptions import *

from ..forms import client as forms

class ClientList( ListView ):
	template_name = 'pages/org/client/index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Organization.objects.get( refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid' ], **kwargs )
		obj_list = Client.objects.filter( organization__refnum = mid.oid )
		return obj_list
	
	def _create_object( self, request, data, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid' ], **kwargs )
		org = Organization.objects.get( refnum = mid.oid )
		return ClientBusLog.create( org, data[ 'trading_name' ] )


	def create_object_html( self, request, data, *args, **kwargs ):
		form = forms.AddClient( data or None )
		if form.is_valid() is False:
			return redirect( 'org-client-list', oid = self.url_kwargs.oid )

		try:
			newo = self._create_object( request, form.cleaned_data, *args, **kwargs )
		except BusLogError, berror:
			messages.error( request, berror.message )
			return redirect( 'org-client-list', oid = self.url_kwargs.oid )

		messages.success( request, '<a href="{}">{}</a> was added as a new client.'.format( newo.get_single_url(), newo.trading_name ) )
		return redirect( 'org-client-list', oid = self.url_kwargs.oid )

	def create_object_json( self, request, data, *args, **kwargs ):
		newo = self._create_object( request, data, *args, **kwargs )
		resp = { 'url' : reverse( 'org-client-single', kwargs = { 'oid' : newo.organization.refnum, 'cid' : newo.refnum } ) }
		return self.api_resp( resp )




class ClientSingle( SingleObjectView ):
	template_name = 'pages/org/client/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid' ], **kwargs )
		return get_object_or_404( Client, refnum = mid.cid, organization__refnum = mid.oid )

	def delete_object( self, request, ob, *args, **kwargs ):
		ob.delete()
		return redirect( 'org-client-list', oid = ob.organization.refnum )

	def update_object_json( self, request, obj, data, *args, **kwargs ):
		obj.trading_name = data.get( 'trading_name', obj.trading_name )
		obj.save()
		return redirect( 'org-client-single', oid = obj.organization.refnum, cid = obj.refnum )


