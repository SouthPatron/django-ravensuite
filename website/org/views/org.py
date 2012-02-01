from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from django.conf import settings
from django.http import HttpResponseForbidden

from common.views.singleobjectview import SingleObjectView
from common.views.listview import ListView

from common.models import *

from ..forms import org as forms

from common.buslog.org.org import *
from common.buslog.org.user import *
from common.exceptions import *


class OrgList( ListView ):
	template_name = 'pages/org/org/index'

	def get_object_list( self, request, *args, **kwargs ):
		umems = UserMembership.objects.filter( user = request.user )

		newobj_list = []
		for obj in umems:
			org = obj.organization
			org.membership = obj
			newobj_list.append( org )

		return newobj_list

	def create_object_html( self, request, data, *args, **kwargs ):
		form = forms.CreateOrganization( data or None )
		if form.is_valid() is False:
			return redirect( 'org-list' )

		try:
			neworg = self._create_object( request, form.cleaned_data, *args, **kwargs )
		except BLE_Error, berror:
			messages.error( request, berror.message )
			return redirect( 'org-list' )

		messages.success( request, 'Created new organization <a href="{}">{}</a>'.format( neworg.get_single_url(), neworg.trading_name ) )

		return redirect( 'org-list' )

	def create_object_json( self, request, data, *args, **kwargs ):
		neworg = self._create_object( request, data, *args, **kwargs )
		resp = { 'url' : reverse( 'org-single', kwargs = { 'oid' : neworg.refnum } ) }
		return self.api_resp( resp )


	def _create_object( self, request, data, *args, **kwargs ):
		neworg = OrgBusLog.create( request.user, data[ 'trading_name' ] )
		UserBusLog.grant( request.user, neworg, UserCategory.OWNER )
		return neworg




class OrgSingle( SingleObjectView ):
	template_name = 'pages/org/org/single'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Organization, refnum = self.url_kwargs.oid )

	def delete_object( self, request, ob, *args, **kwargs ):
		ob.delete()
		return redirect( 'org-list' )

	def update_object_html( self, request, obj, data, *args, **kwargs ):
		self._update_object( request, obj, data, *args, **kwargs )
		return redirect( 'org-single', oid = obj.refnum )

	def update_object_json( self, request, obj, data, *args, **kwargs ):
		self._update_object( request, obj, data, *args, **kwargs )
		resp = { 'url' : reverse( 'org-single', kwargs = { 'oid' : neworg.refnum } ) }
		return self.api_resp( resp )

	def _update_object( self, request, obj, data, *args, **kwargs ):
		obj.trading_name = data.get( 'trading_name', obj.trading_name )
		obj.save()


class OrgTestSingle( SingleObjectView ):
	template_name = 'pages/org/org/test'

	def get_object( self, request, *args, **kwargs ):
		return { 'hello' : True }




