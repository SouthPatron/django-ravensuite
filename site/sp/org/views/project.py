from django.shortcuts import get_object_or_404, redirect

from common.views.pageview import PageView
from common.models import *


class ProjectList( PageView ):
	template_name = 'pages/org/client/project/index'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Client, refnum = self.url_kwargs.cid, organization__refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = Project.objects.filter( client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid )
		return obj_list
	

class ProjectSingle( PageView ):
	template_name = 'pages/org/client/project/single'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Project, refnum = self.url_kwargs.pid, client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid )

