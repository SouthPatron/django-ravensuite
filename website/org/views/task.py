from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect

from singleobjectview import SingleObjectView
from listview import ListView

from ..models import *

from ..forms import task as forms

class TaskList( ListView ):
	template_name = 'pages/org/task/index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Activity.objects.get( id = self.url_kwargs.actid )

	def get_object_list( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'actid' ], **kwargs )
		obj_list = Task.objects.filter( activity__id = mid.actid, activity__organization__refnum = mid.oid )
		return obj_list
	
	def _create_object( self, request, data, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'actid' ], **kwargs )

		newtask = Task()
		newtask.activity = Activity.objects.get( id = mid.actid, organization__refnum = mid.oid )
		newtask.name = data[ 'name' ]
		newtask.description = data[ 'description' ]
		newtask.save()

		return newtask

	def create_object_html( self, request, data, *args, **kwargs ):
		form = forms.CreateTask( data or None )
		if form.is_valid() is False:
			return redirect( 'org-activity-task-list', oid = self.url_kwargs.oid )
		newo = self._create_object( request, form.cleaned_data, *args, **kwargs )
		return redirect( newo.get_single_url() )

	def create_object_json( self, request, data, *args, **kwargs ):
		newo = self._create_object( request, data, *args, **kwargs )
		resp = { 'url' : newo.get_single_url() }
		return self.api_resp( resp )




class TaskSingle( SingleObjectView ):
	template_name = 'pages/org/task/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'actid', 'taskid' ], **kwargs )
		return get_object_or_404( Task, id = mid.taskid, activity__id = mid.actid, activity__organization__refnum = mid.oid )

	def delete_object( self, request, ob, *args, **kwargs ):
		ob.delete()
		return redirect( 'org-activity-task-list', oid = ob.get_org().refnum, actid = ob.get_activity().id )

	def update_object_json( self, request, obj, data, *args, **kwargs ):
		obj.name = data.get( 'name', obj.name )
		obj.description = data.get( 'description', obj.description )
		obj.save()
		return redirect( obj.get_single_url() )


