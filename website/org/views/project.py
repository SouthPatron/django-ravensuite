from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from common.views.singleobjectview import SingleObjectView
from common.views.listview import ListView

from common.models import *
from common.buslog.org import *
from common.exceptions import *

from ..forms import project as forms

class ProjectList( ListView ):
	template_name = 'pages/org/project/index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = Project.objects.filter( client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid )
		return obj_list
	
	def _create_object( self, request, data, *args, **kwargs ):

		client = Client.objects.get( refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

		newo = ProjectBusLog.create(
					client,
					data.get( 'status', ProjectStatus.INACTIVE ),
					data.get( 'name' ),
					data.get( 'description' ),
				)

		return newo


	def create_object_json( self, request, data, *args, **kwargs ):
		newo = self._create_object( self, request, data, *args, **kwargs )
		resp = { 'url' : newo.get_single_url() }
		return self.api_resp( resp )

	def create_object_html( self, request, data, *args, **kwargs ):
		form = forms.CreateProject( data or None )
		if form.is_valid() is False:
			for field in form:
				messages.error( request, field.errors )
			return redirect( 'org-client-project-list', oid = self.url_kwargs.oid, cid = self.url_kwargs.cid )

		try:
			newo = self._create_object( request, form.cleaned_data, *args, **kwargs )
		except BusLogError, berror:
			messages.error( request, berror.message )
			return redirect( 'org-client-project-list', oid = self.url_kwargs.oid, cid = self.url_kwargs.cid )

		messages.success( request, 'Project <a href="{}">{}</a> was successfully created.'.format( newo.get_single_url(), newo.name ) )
		return redirect( 'org-client-project-list', oid = self.url_kwargs.oid, cid = self.url_kwargs.cid )






class ProjectSingle( SingleObjectView ):
	template_name = 'pages/org/project/single'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Project, refnum = self.url_kwargs.pid, client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid )

	def delete_object( self, request, ob, *args, **kwargs ):
		ob.delete()
		return redirect( 'org-client-project-list', cid = ob.client.refnum, oid = ob.client.organization.refnum )

	def update_object_json( self, request, obj, data, *args, **kwargs ):
		obj.status = data.get( 'status', obj.status )
		obj.name = data.get( 'name', obj.name )
		obj.description = data.get( 'name', obj.description )
		obj.save()
		return redirect( 'org-client-project-single', oid = obj.client.organization.refnum, cid = obj.client.refnum, pid = obj.refnum )



