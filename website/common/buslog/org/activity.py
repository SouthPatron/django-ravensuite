from __future__ import unicode_literals

from common.models import *


class ActivityBusLog( object ):

	@staticmethod
	def create( org, name, description ):

		newact = Activity()
		newact.organization = organization
		newact.name = name
		newact.description = description
		newact.save()

		return newact


