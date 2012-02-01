from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from common.models import *
from common.exceptions import *


class TaskBusLog( object ):

	@staticmethod
	def create( activity, name, description ):

		try:
			newtask = Task.objects.get( activity = activity, name = name )
			raise BLE_ConflictError( _('BLE_50005') )
		except Task.DoesNotExist:
			pass

		newtask = Task()
		newtask.activity = activity
		newtask.name = name
		newtask.description = description
		newtask.save()

		return newtask


