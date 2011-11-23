from __future__ import unicode_literals

from common.models import *
from common.exceptions import *


class ActivityBusLog( object ):

	@staticmethod
	def create( org, name, description ):

		try:
			newacc = Activity.objects.get( organization = org, name = name )
			raise BusLogError( 'An activity with that name already exists' )
		except Activity.DoesNotExist:
			pass

		newact = Activity()
		newact.organization = org
		newact.name = name
		newact.description = description
		newact.save()

		return newact


