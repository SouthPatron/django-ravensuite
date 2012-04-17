from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from common.views.modal import ModalLogic
from common.models import *

from common.exceptions import *
from common.utils.dbgdatetime import datetime


from ..forms.timer import NewTimer as NewTimerForm


class NewTimer( ModalLogic ):

	def get_extra( self, request, dmap, obj, *args, **kwargs ):

		extra = {}

		extra[ 'organization' ] = Organization.objects.all()

		if 'oid' in dmap and dmap['oid'] != "":
			extra[ 'client' ] = Client.objects.filter( organization__refnum = dmap['oid'] )

			if 'cid' in dmap and dmap['cid'] != "":
				extra[ 'project' ] = Project.objects.filter( client__refnum = dmap['cid'], client__organization__refnum = dmap[ 'oid' ] )

				if 'pid' in dmap and dmap['pid'] != "":
					extra[ 'activity' ] = Activity.objects.filter( organization__refnum = dmap[ 'oid' ] )

					if 'actid' in dmap and dmap['actid']:
						extra[ 'task' ] = Task.objects.filter( activity = dmap['actid' ], activity__organization__refnum = dmap[ 'oid' ] )


		# user

		# organization
		# client
		# project
		# activity
		# task

		# comment

		# start_time
		# seconds


		return extra

	def get_object( self, request, dmap, *args, **kwargs ):
		return None


	def perform( self, request, dmap, obj, extra, fmt, *args, **kwargs ):

		pdata = dmap

		tse = TimesheetEntry()
		tse.user = request.user
		tse.project = Project.objects.get( refnum = pdata[ 'project' ], client__refnum = pdata[ 'client' ], client__organization__refnum = pdata[ 'organization' ] )
		tse.task = Task.objects.get( id = pdata[ 'task' ], activity__id = pdata[ 'activity' ] )
		tse.comment = pdata.get( 'comment', tse.task.name )

		hour = pdata[ 'start_time_hour' ]
		minute = pdata[ 'start_time_minute' ]

		now = datetime.datetime.now()

		tse.start_time = datetime.datetime( now.year, now.month, now.day, int(hour), int(minute) )

		if 'running_timer' not in pdata:

			end_hour = pdata[ 'end_time_hour' ]
			end_minute = pdata[ 'end_time_minute' ]

			end_time = datetime.datetime( now.year, now.month, now.day, int(end_hour), int(end_minute) )

			difference = end_time - tse.start_time
			tse.seconds = abs(difference.total_seconds())
			tse.save()

			self.easy.refresh()
			return tse


		tse.save()

		timer = TimesheetTimer()
		timer.timesheet_entry = tse
		timer.start_time = now
		timer.save()

		self.easy.refresh()
		return tse


