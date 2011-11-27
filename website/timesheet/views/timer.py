from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from common.views.listview import ListView
from common.views.singleobjectview import SingleObjectView
from common.models import *

from common.buslog.timesheet.timer import TimerBusLog
from common.exceptions import *

from ..forms import timer as forms


class TimerList( ListView ):
	template_name = 'pages/timesheet/timer/index'

#	def get_extra( self, request, *args, **kwargs ):
#		return TimesheetEntry.objects.filter( user = request.user ).latest( 'end_time' )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = TimesheetTimer.objects.filter( user = request.user )
		return obj_list

	def _create_object( self, request, data, *args, **kwargs ):
		return TimerBusLog.start_timer(
					request.user,
					data[ 'project' ],
					data[ 'task' ],
					data[ 'description' ]
				)

	def create_object_html( self, request, data, *args, **kwargs ):
		form = forms.NewTimer( data or None )
		if form.is_valid() is False:
			return redirect( 'timesheet-timer-list' )

		try:
			newo = self._create_object( request, form.cleaned_data, *args, **kwargs )
		except BusLogError, berror:
			messages.error( request, berror.message )
			return redirect( 'timesheet-timer-list' )

		messages.success( request, 'Timer has started.' )
		return redirect( 'timesheet-timer-list' )



class TimerSingle( SingleObjectView ):
	template_name = 'pages/timesheet/timer/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'timerid' ], **kwargs )
		return get_object_or_404( TimesheetTimer, id = mid.timerid )

	def delete_object( self, request, ob, *args, **kwargs ):
		ob.delete()
		return redirect( 'timesheet-timer-list' )

	def _update_object( self, request, obj, data, *args, **kwargs ):

		obj.project = data.get( 'project', obj.project )
		obj.task = data.get( 'task', obj.task )
		obj.description = data.get( 'description', obj.description )

		aksie = data.get( 'action', None )

		if aksie is None:
			obj.save()
			return

		if aksie == 'stop':
			TimerBusLog.stop_timer( request.user, obj.project )
			return


	def update_object_html( self, request, obj, data, *args, **kwargs ):
		self._update_object( request, obj, data, *args, **kwargs )
		return redirect( 'timesheet-timer-list' )

	def update_object_json( self, request, obj, data, *args, **kwargs ):
		self._update_object( request, obj, data, *args, **kwargs )
		resp = { 'url' : reverse( 'timesheet-timer-single', kwargs = { 'timerid' : obj.id } ) }
		return self.api_resp( resp )


