from __future__ import unicode_literals

from common.models import *
from common.exceptions import *

from common.utils.dbgdatetime import datetime


class AccountBusLog( object ):

	@staticmethod
	def adjust( account, event_time, group, description, amount, source_document, data ):

		# TODO: account should be locked whilst adjusting and reading

		new_balance = account.balance + amount

		transaction = AccountTransaction()
		transaction.account = account
		transaction.refnum = account.transaction_no
		transaction.creation_time = datetime.datetime.now()
		transaction.event_time = event_time
		transaction.group = group
		transaction.description = description
		transaction.balance_before = account.balance
		transaction.balance_after = new_balance
		transaction.amount = amount
		transaction.source_document = source_document
		transaction.save()

		tdata = AccountTransactionData()
		tdata.account_transaction = transaction
		tdata.data = data
		tdata.save()

		account.transaction_no += 1
		account.balance = new_balance
		account.save()

		return transaction


