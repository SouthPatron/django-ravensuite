from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from common.views.singleobjectview import SingleObjectView
from common.views.listview import ListView

from common.models import *

from common.buslog.org import *

from ..forms import activity as forms

class ActivityList( ListView ):
	template_name = 'pages/org/activity/index'

	def get_object( self, request, obj_list, fmt, *args, **kwargs ):
		return Organization.objects.get( refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = Activity.objects.filter( organization__refnum = self.url_kwargs.oid )
		return obj_list
	
	def _create_object( self, request, data, *args, **kwargs ):

		org = Organization.objects.get( refnum = self.url_kwargs.oid )
		newact = ActivityBusLog.create( org, data[ 'name' ], data[ 'description' ] )
		return newact

	def create_object_html( self, request, data, *args, **kwargs ):
		form = forms.CreateActivity( data or None )
		if form.is_valid() is False:
			return redirect( 'org-activity-list', oid = self.url_kwargs.oid )

		try:
			newo = self._create_object( request, form.cleaned_data, *args, **kwargs )
		except BLE_Error, berror:
			messages.error( request, berror.message )
			return redirect( 'org-activity-list', oid = self.url_kwargs.oid )

		messages.success( request, _('VMG_20001') % { 'url' : newo.get_absolute_url(), 'name' : newo.name } )
		return redirect( 'org-activity-list', oid = self.url_kwargs.oid )



	def create_object_json( self, request, data, *args, **kwargs ):
		newo = self._create_object( request, data, *args, **kwargs )
		resp = { 'url' : reverse( 'org-activity-single', kwargs = { 'oid' : newo.organization.refnum, 'actid' : newo.id } ) }
		return self.api_resp( resp )




class ActivitySingle( SingleObjectView ):
	template_name = 'pages/org/activity/single'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Activity, id = self.url_kwargs.actid, organization__refnum = self.url_kwargs.oid )

	def delete_object( self, request, ob, *args, **kwargs ):
		ob.delete()
		return redirect( 'org-activity-list', oid = ob.organization.refnum )

	def update_object_json( self, request, obj, data, *args, **kwargs ):
		obj.name = data.get( 'name', obj.name )
		obj.description = data.get( 'description', obj.description )
		obj.save()
		return redirect( 'org-activity-single', oid = obj.organization.refnum, actid = obj.refnum )


