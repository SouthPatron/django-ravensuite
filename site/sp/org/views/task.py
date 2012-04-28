from django.shortcuts import get_object_or_404, redirect

from common.views.pageview import PageView
from common.models import *


class TaskList( PageView ):
	template_name = 'pages/org/activity/task/index'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Activity, id = self.url_kwargs.actid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = Task.objects.filter( activity__id = self.url_kwargs.actid, activity__organization__refnum = self.url_kwargs.oid )
		return obj_list
	

class TaskSingle( PageView ):
	template_name = 'pages/org/activity/task/single'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Task, id = self.url_kwargs.taskid, activity__id = self.url_kwargs.actid, activity__organization__refnum = self.url_kwargs.oid )

