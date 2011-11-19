from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect

from singleobjectview import SingleObjectView
from listview import ListView

from ..models import *

from ..forms import user as forms

from website.account.support import AccountSupport
from common.utils.email import send_templated_email


class UserList( ListView ):
	template_name = 'pages/org/user/index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Organization.objects.get( refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid' ], **kwargs )
		obj_list = UserMembership.objects.filter( organization__refnum = mid.oid )
		return obj_list
	
	def _create_object( self, request, data, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid' ], **kwargs )

		wasNewUser = False

		try:
			the_user = User.objects.get( email = data[ 'email_address' ] )
		except User.DoesNotExist:
			new_password = User.objects.make_random_password()
			the_user = AccountSupport.create( data[ 'email_address'], new_password, data[ 'first_name' ], data[ 'last_name' ] )
			wasNewUser = True


		newuser = UserMembership()
		newuser.user = the_user
		newuser.organization = Organization.objects.get( refnum = mid.oid )
		newuser.category = data[ 'category' ]
		newuser.is_enabled = True
		newuser.save()

		if wasNewUser is True:
			send_templated_email( the_user, 'org', 'user_added', { 'password' : new_password, 'organization' : newuser.organization } )

		return newuser

	def create_object_html( self, request, data, *args, **kwargs ):
		form = forms.AddUser( data or None )
		if form.is_valid() is False:
			return redirect( 'org-user-list', oid = self.url_kwargs.oid )

		newo = self._create_object( request, form.cleaned_data, *args, **kwargs )
		return redirect( newo.get_single_url() )

	def create_object_json( self, request, data, *args, **kwargs ):
		newo = self._create_object( request, data, *args, **kwargs )
		resp = { 'url' : newo.get_single_url() }
		return self.api_resp( resp )



class UserSingle( SingleObjectView ):
	template_name = 'pages/org/user/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'uid' ], **kwargs )
		return get_object_or_404( UserMembership, id = mid.uid, organization__refnum = mid.oid )

	def delete_object( self, request, ob, *args, **kwargs ):
		ob.delete()
		return redirect( 'org-user-list', oid = ob.organization.refnum )

	def update_object_json( self, request, obj, data, *args, **kwargs ):
		obj.category = data.get( 'category', obj.category )
		obj.is_enabled = data.get( 'is_enabled', obj.is_enabled )
		obj.save()
		return redirect( obj.get_single_url() )


