from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from common.views.modal import ModalLogic
from common.models import *

from common.exceptions import *


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



