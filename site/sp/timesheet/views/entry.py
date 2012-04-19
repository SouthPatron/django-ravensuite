from common.views.pageview import PageView
from common.models import *

class TimesheetEntryList( PageView ):
	template_name = 'pages/timesheet/entry/index'

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = TimesheetEntry.objects.filter( user = request.user )
		return obj_list



