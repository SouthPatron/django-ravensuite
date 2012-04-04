from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from common.models import *
from common.exceptions import *


class ProjectBusLog( object ):

	@staticmethod
	def get_next_refnum( org ):
		# TODO: make safe in case two are created
		sc = org.organizationcounter
		refnum = sc.project_no
		sc.project_no += 1
		sc.save()
		return refnum


	@staticmethod
	def create( client, status, name, description ):

		try:
			newproj = Project.objects.get( name = name, client = client )

			raise BLE_ConflictError( _('BLE_50004') )
		except Project.DoesNotExist:
			pass


		refnum = ProjectBusLog.get_next_refnum( client.organization )

		newproj = Project()
		newproj.client = client
		newproj.refnum = refnum
		newproj.status = status
		newproj.name = name
		newproj.description = description
		newproj.save()

		return newproj

