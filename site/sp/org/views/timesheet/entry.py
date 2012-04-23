from django.shortcuts import get_object_or_404

from common.views.pageview import PageView
from common.models import *

class TimesheetEntryList( PageView ):
	template_name = 'pages/org/timesheet/entry/index'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Organization, refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = TimesheetEntry.objects.filter( user = request.user )
		return obj_list



