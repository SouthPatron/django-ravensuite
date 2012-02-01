from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from common.models import *
from common.exceptions import *


class ActivityBusLog( object ):

	@staticmethod
	def create( org, name, description ):

		try:
			newacc = Activity.objects.get( organization = org, name = name )
			raise BLE_ConflictError( _('BLE_50001') )
		except Activity.DoesNotExist:
			pass

		newact = Activity()
		newact.organization = org
		newact.name = name
		newact.description = description
		newact.save()

		return newact


