from __future__ import unicode_literals

from common.models import *
from common.exceptions import *


class TabBusLog( object ):

	@staticmethod
	def get_next_refnum():
		# TODO: select_for_update()
		sc = SystemCounter.objects.get( id = 1 )
		refnum = sc.tab_no
		sc.tab_no += 1
		sc.save()
		return refnum


	@staticmethod
	def create( client, name, min_balance ):

		try:
			newacc = Tab.objects.get( client = client, name = name )
			raise BusLogError( 'A tab with that name already exists' )
		except Tab.DoesNotExist:
			pass


		refnum = TabBusLog.get_next_refnum()

		newtab = Tab()
		newtab.client = client
		newtab.refnum = refnum
		newtab.is_enabled = True
		newtab.name = name
		newtab.min_balance = min_balance
		newtab.save()

		return newtab


