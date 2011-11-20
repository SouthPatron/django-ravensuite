from __future__ import unicode_literals

from common.models import *


class TaskBusLog( object ):

	@staticmethod
	def create( activity, name, description ):

		newtask = Task()
		newtask.activity = activity
		newtask.name = name
		newtask.description = description
		newtask.save()

		return newtask


