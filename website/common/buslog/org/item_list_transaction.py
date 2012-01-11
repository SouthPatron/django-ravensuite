from __future__ import unicode_literals

from math import *
from copy import deepcopy

from common.models import *
from common.exceptions import *
from common.buslog.org import AccountBusLog
from common.moe import MarginsOfError
from common.utils.dbgdatetime import datetime
from common.utils.objroute import *
from common.utils.parse import *


class ItemListTransactionBusLog( object ):

	@staticmethod
	def get_next_refnum( org ):
		# TODO: select_for_update()
		sc = OrganizationCounter.objects.get( organization__refnum = org.refnum )
		refnum = sc.item_list_transaction_no
		sc.item_list_transaction_no += 1
		sc.save()
		return refnum


	@staticmethod
	def create( client, document_type, document_state ):
		newt = ItemListTransaction()
		newt.client = client
		newt.refnum = ItemListTransactionBusLog.get_next_refnum( client.get_org() )
		newt.creation_time = datetime.datetime.now()
		newt.document_type = document_type
		newt.document_state = document_state

		newt.save()
		return newt

	@staticmethod
	def delete( obj ):
		obj.delete()

	@staticmethod
	def	set_meta( obj, key, value ):
		sam = ItemListMeta(
				item_list_transaction = obj,
				key = key,
				value = '{}'.format( value )
			)
		sam.save()

	@staticmethod
	def get_meta( obj, key, default = None ):
		rc = ItemListMeta.objects.filter(
				item_list_transaction = obj,
				key = key
			)
		if rc.count() == 0:
			if default is not None:
				return default
			raise RuntimeError( 'No results found' )

		if rc.count() > 1:
			raise RuntimeError( 'Too many results returned' )

		return rc[0]
	
	@staticmethod
	def clear_meta( obj ):
		ItemListMeta.objects.filter( item_list_transaction = obj ).delete()

	@staticmethod
	def get_all_meta( obj ):
		return ItemListMeta.objects.filter( item_list_transaction = obj )


	@staticmethod
	def add_line( obj, description, units, perunit, tax_rate ):

		my_total = 0
		my_tax = 0
		# TODO: dynamic tax rate
		my_tax_rate = 0.14

		multiple = long( units * perunit / 100 )

		if tax_rate == TaxRate.NONE or tax_rate == TaxRate.EXEMPT:
			my_total = multiple
			my_tax = 0
		elif tax_rate == TaxRate.EXCLUSIVE:
			temp_tax = long( multiple * my_tax_rate )
			my_total = multiple + temp_tax
			my_tax = temp_tax
		elif tax_rate == TaxRate.INCLUSIVE:
			my_total = multiple
			my_tax = multiple - long(long( multiple * 100 / (1 + my_tax_rate) ) / 100)

		sam = ItemListLine(
				item_list_transaction = obj,
				description = description,
				units = units,
				perunit = perunit,
				tax_rate = tax_rate,
				tax_amount = my_tax,
				total = my_total
			)
		sam.save()



	@staticmethod
	def clear_lines( obj ):
		ItemListLine.objects.filter( item_list_transaction = obj ).delete()

		obj.amount = 0
		obj.tax = 0
		obj.total = 0

		obj.save()


	@staticmethod
	def get_lines( obj ):
		return ItemListLine.objects.filter( item_list_transaction = obj )



