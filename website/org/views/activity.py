from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect

from singleobjectview import SingleObjectView
from listview import ListView

from ..models import *

from ..forms import activity as forms

class ActivityList( ListView ):
	template_name = 'pages/org/activity/index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Organization.objects.get( refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid' ], **kwargs )
		obj_list = Activity.objects.filter( organization__refnum = mid.oid )
		return obj_list
	
	def _create_object( self, request, data, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid' ], **kwargs )

		newactivity = Activity()
		newactivity.organization = Organization.objects.get( refnum = mid.oid )
		newactivity.name = data[ 'name' ]
		newactivity.description = data[ 'description' ]
		newactivity.save()

		return newactivity

	def create_object_html( self, request, data, *args, **kwargs ):
		form = forms.CreateActivity( data or None )
		if form.is_valid() is False:
			return redirect( 'org-activity-list', oid = self.url_kwargs.oid )

		newo = self._create_object( request, form.cleaned_data, *args, **kwargs )
		return redirect( 'org-activity-single', oid = newo.organization.refnum, actid = newo.id )

	def create_object_json( self, request, data, *args, **kwargs ):
		newo = self._create_object( request, data, *args, **kwargs )
		resp = { 'url' : reverse( 'org-activity-single', kwargs = { 'oid' : newo.organization.refnum, 'actid' : newo.id } ) }
		return self.api_resp( resp )




class ActivitySingle( SingleObjectView ):
	template_name = 'pages/org/activity/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'actid' ], **kwargs )
		return get_object_or_404( Activity, id = mid.actid, organization__refnum = mid.oid )

	def delete_object( self, request, ob, *args, **kwargs ):
		ob.delete()
		return redirect( 'org-activity-list', oid = ob.organization.refnum )

	def update_object_json( self, request, obj, data, *args, **kwargs ):
		obj.name = data.get( 'name', obj.name )
		obj.description = data.get( 'description', obj.description )
		obj.save()
		return redirect( 'org-activity-single', oid = obj.organization.refnum, actid = obj.refnum )


