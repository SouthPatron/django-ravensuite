from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from django.utils.html import escape
from django.shortcuts import get_object_or_404, redirect

from common.views.singleobjectview import SingleObjectView
from common.views.listview import ListView
from django.contrib import messages

from common.models import *

from ..forms import user as forms

from common.buslog.org import UserBusLog
from common.exceptions import *


class UserList( ListView ):
	template_name = 'pages/org/admin/user/index'

	def get_object( self, request, obj_list, fmt, *args, **kwargs ):
		return Organization.objects.get( refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = UserMembership.objects.filter( organization__refnum = self.url_kwargs.oid )
		return obj_list
	
	def _create_object( self, request, data, *args, **kwargs ):

		try:
			newgrant = UserBusLog.invite_user( 
							data[ 'first_name' ],
							data[ 'last_name' ],
							data[ 'email_address' ],
							Organization.objects.get( refnum = self.url_kwargs.oid ),
							data[ 'category' ]
						)
		except BLE_Error, berror:
			messages.error( request, berror.message )
			return redirect( 'org-list' )

		messages.success(
			request,
			_( 'VMG_20010' ) % 
			{
				'url' : escape(newgrant.get_absolute_url()),
				'first_name' : newgrant.user.first_name,
				'last_name' : newgrant.user.last_name
			}
		)

		return newgrant

	def create_object_html( self, request, data, *args, **kwargs ):
		form = forms.AddUser( data or None )
		if form.is_valid() is False:
			return redirect( 'org-admin-user-list', oid = self.url_kwargs.oid )

		newo = self._create_object( request, form.cleaned_data, *args, **kwargs )
		return redirect( 'org-admin-user-list', oid = self.url_kwargs.oid )

	def create_object_json( self, request, data, *args, **kwargs ):
		newo = self._create_object( request, data, *args, **kwargs )
		resp = { 'url' : newo.get_absolute_url() }
		return self.api_resp( resp )



class UserSingle( SingleObjectView ):
	template_name = 'pages/org/admin/user/single'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( UserMembership, id = self.url_kwargs.uid, organization__refnum = self.url_kwargs.oid )

	def delete_object( self, request, ob, *args, **kwargs ):
		ob.delete()
		return redirect( 'org-admin-user-list', oid = ob.organization.refnum )

	def update_object_json( self, request, obj, data, *args, **kwargs ):
		obj.category = data.get( 'category', obj.category )
		obj.is_enabled = data.get( 'is_enabled', obj.is_enabled )
		obj.save()
		return redirect( obj.get_absolute_url() )


