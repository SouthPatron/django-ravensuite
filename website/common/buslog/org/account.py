from __future__ import unicode_literals

from common.models import *
from common.exceptions import *

from common.utils.dbgdatetime import datetime


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

		try:
			newacc = Account.objects.get( client = client, name = name )
			raise BusLogError( 'An account with that name already exists' )
		except Account.DoesNotExist:
			pass

		refnum = AccountBusLog.get_next_refnum()

		newacc = Account()
		newacc.client = client
		newacc.refnum = refnum
		newacc.is_enabled = True
		newacc.name = name
		newacc.min_balance = min_balance
		newacc.save()

		return newacc


	@staticmethod
	def adjust( account, group, description, amount, data ):

		# TODO: account should be locked whilst adjusting and reading

		if account.is_enabled is False:
			raise BusLogError( 'The account is not enabled. Adjustments are not allowed.' )

		new_balance = account.balance + amount

		if amount < 0:
			if new_balance < account.min_balance:
				raise BusLogError( 'The adjustment will exceed the minimum balance limit on the account.' )


		transaction = AccountTransaction()
		transaction.account = account
		transaction.refnum = account.transaction_no
		transaction.event_time = datetime.datetime.now()
		transaction.group = group
		transaction.description = description
		transaction.balance_before = account.balance
		transaction.balance_after = new_balance
		transaction.amount = amount
		transaction.save()

		tdata = AccountTransactionData()
		tdata.account_transaction = transaction
		tdata.data = data
		tdata.save()

		account.transaction_no += 1
		account.balance = new_balance
		account.save()

		return transaction


