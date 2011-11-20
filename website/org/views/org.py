from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse

from django.conf import settings
from django.http import HttpResponseForbidden

from singleobjectview import SingleObjectView
from listview import ListView

from common.models import *

from ..forms import org as forms


class OrgList( ListView ):
	template_name = 'pages/org/org/index'

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = Organization.objects.all()
		return obj_list

	def create_object_html( self, request, data, *args, **kwargs ):
		form = forms.CreateOrganization( data or None )
		if form.is_valid() is False:
			return redirect( 'org-list' )

		neworg = self._create_object( request, form.cleaned_data, *args, **kwargs )
		return redirect( 'org-list' )

	def create_object_json( self, request, data, *args, **kwargs ):
		neworg = self._create_object( request, data, *args, **kwargs )
		resp = { 'url' : reverse( 'org-single', kwargs = { 'oid' : neworg.refnum } ) }
		return self.api_resp( resp )


	def _create_object( self, request, data, *args, **kwargs ):
		# TODO: Use select_for_update()
		sc = SystemCounter.objects.get( id = 1 )
		refnum = sc.organization_no
		sc.organization_no += 1
		sc.save()

		neworg = Organization()
		neworg.trading_name = data[ 'trading_name' ]
		neworg.refnum = refnum
		neworg.save()

		OrganizationCounter.objects.create( organization = neworg )
		OrganizationAccount.objects.create( organization = neworg )

		newuser = UserMembership()
		newuser.user = request.user
		newuser.organization = neworg
		newuser.category = UserCategory.OWNER
		newuser.is_enabled = True
		newuser.save()

		return neworg




class OrgSingle( SingleObjectView ):
	template_name = 'pages/org/org/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid' ], **kwargs )
		return get_object_or_404( Organization, refnum = mid.oid )

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

