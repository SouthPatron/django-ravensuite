from __future__ import unicode_literals

from common.utils.dbgdatetime import datetime

from common.models import *
from common.exceptions import *


class TimerBusLog( object ):

	@staticmethod
	def start_timer( user, project, task, description ):

		try:
			newo = TimesheetTimer.objects.get( user = user, project = project )
			raise BLE_ConflictError( 'There is an existing timer running on that project for the user.' )
		except TimesheetTimer.DoesNotExist:
			pass

		newo = TimesheetTimer()
		newo.user = user
		newo.project = project
		newo.task = task
		newo.start_time = datetime.datetime.now()
		newo.description = description
		newo.save()

		return newo

	@staticmethod
	def delete_timer( user, project ):

		try:
			newo = TimesheetTimer.objects.get( user = user, project = project  )
		except TimesheetTimer.DoesNotExist:
			raise BLE_NotFoundError( 'There is no timer running for that user on that project.' )

		newo.delete()
		return newo


	@staticmethod
	def stop_timer( user, project ):

		try:
			newo = TimesheetTimer.objects.get( user = user, project = project  )
		except TimesheetTimer.DoesNotExist:
			raise BLE_NotFoundError( 'There is no timer running for that user on that project.' )

		timo = TimesheetEntry()
		timo.user = newo.user
		timo.project = newo.project
		timo.task = newo.task
		timo.start_time = newo.start_time
		timo.description = newo.description
		timo.end_time = datetime.datetime.now()
		timo.save()

		newo.delete()
		return timo


