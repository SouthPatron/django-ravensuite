from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect

from common.views.listview import ListView
from common.models import *


class EntryList( ListView ):
	template_name = 'pages/timesheet/entry/index'

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = TimesheetEntry.objects.filter( user = request.user )
		return obj_list



