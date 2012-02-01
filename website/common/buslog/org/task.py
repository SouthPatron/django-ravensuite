from __future__ import unicode_literals

from common.models import *
from common.exceptions import *


class TaskBusLog( object ):

	@staticmethod
	def create( activity, name, description ):

		try:
			newtask = Task.objects.get( activity = activity, name = name )
			raise BLE_ConflictError( 'A task with that name already exists' )
		except Task.DoesNotExist:
			pass

		newtask = Task()
		newtask.activity = activity
		newtask.name = name
		newtask.description = description
		newtask.save()

		return newtask


