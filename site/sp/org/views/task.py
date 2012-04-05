from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from common.views.singleobjectview import SingleObjectView
from common.views.listview import ListView

from common.models import *
from common.buslog.org import *

from ..forms import task as forms

class TaskList( ListView ):
	template_name = 'pages/org/activity/task/index'

	def get_object( self, request, obj_list, fmt, *args, **kwargs ):
		return Activity.objects.get( id = self.url_kwargs.actid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = Task.objects.filter( activity__id = self.url_kwargs.actid, activity__organization__refnum = self.url_kwargs.oid )
		return obj_list
	
	def _create_object( self, request, data, *args, **kwargs ):

		newtask = TaskBusLog.create( 
						Activity.objects.get( id = self.url_kwargs.actid, organization__refnum = self.url_kwargs.oid ),
						data[ 'name' ],
						data[ 'description' ],
					)

		return newtask

	def create_object_html( self, request, data, *args, **kwargs ):
		form = forms.CreateTask( data or None )
		if form.is_valid() is False:
			return redirect( 'org-activity-task-list', oid = self.url_kwargs.oid, actid = self.url_kwargs.actid )

		try:
			newo = self._create_object( request, form.cleaned_data, *args, **kwargs )
		except BLE_Error, berror:
			messages.error( request, berror.message )
			return redirect( 'org-activity-task-list', oid = self.url_kwargs.oid, actid = self.url_kwargs.actid )

		messages.success( request, _('VMG_20009') % { 'url' : newo.get_absolute_url(), 'name' : newo.name } )
		return redirect( 'org-activity-task-list', oid = self.url_kwargs.oid, actid = self.url_kwargs.actid )



	def create_object_json( self, request, data, *args, **kwargs ):
		newo = self._create_object( request, data, *args, **kwargs )
		resp = { 'url' : newo.get_absolute_url() }
		return self.api_resp( resp )




class TaskSingle( SingleObjectView ):
	template_name = 'pages/org/activity/task/single'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Task, id = self.url_kwargs.taskid, activity__id = self.url_kwargs.actid, activity__organization__refnum = self.url_kwargs.oid )

	def delete_object( self, request, ob, *args, **kwargs ):
		ob.delete()
		return redirect( 'org-activity-task-list', oid = ob.get_org().refnum, actid = ob.get_activity().id )

	def update_object_json( self, request, obj, data, *args, **kwargs ):
		obj.name = data.get( 'name', obj.name )
		obj.description = data.get( 'description', obj.description )
		obj.save()
		return redirect( obj.get_absolute_url() )


