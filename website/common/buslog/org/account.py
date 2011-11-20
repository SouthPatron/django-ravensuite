from __future__ import unicode_literals

from common.models import *


class AccountBusLog( object ):

	@staticmethod
	def get_next_refnum():
		# TODO: select_for_update()
		sc = SystemCounter.objects.get( id = 1 )
		refnum = sc.account_no
		sc.account_no += 1
		sc.save()
		return refnum


	@staticmethod
	def create( client, name, min_balance ):

		refnum = AccountBusLog.get_next_refnum()

		newacc = Account()
		newacc.client = client
		newacc.refnum = refnum
		newacc.is_enabled = True
		newacc.name = name
		newacc.min_balance = min_balance
		newacc.save()

		return newacc



