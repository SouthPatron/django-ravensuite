from __future__ import unicode_literals

from math import *
from copy import deepcopy

from common.models import *
from common.exceptions import *
from common.buslog.org import AccountBusLog
from common.buslog.org import ItemListTransactionBusLog as iltb
from common.moe import MarginsOfError
from common.utils.dbgdatetime import datetime
from common.utils.objroute import *
from common.utils.parse import *


class InvoiceBusLog( object ):


	@staticmethod
	def create( client ):
		newt = iltb.create( client, ItemListType.INVOICE, ItemListState.DRAFT )

		iltb.set_meta( newt, "invoice_date", datetime.date.today() )
		iltb.set_meta( newt, "due_date", datetime.date.today() + datetime.timedelta( weeks = 4 ) )
		iltb.set_meta( newt, "comment", "" )

		newt.save()
		return newt

	@staticmethod
	def delete( invoice ):

		if invoice.state == ItemListState.FINAL:
			raise BusLogError( 'This invoice has already been finalized. Try voiding it instead.' )
		if invoice.state == ItemListState.VOID:
			raise BusLogError( 'This invoice has already been voided. It can not be removed.' )

		ItemListTransactionBusLog.delete( invoice )


	@staticmethod
	def _update_sanitize_dates( invoice, new_data ):
		try:
			if new_data[ 'invoice_date' ] is not None:
				new_data[ 'invoice_date' ] = pdateparse( new_data[ 'invoice_date' ] )
			else:
				new_data[ 'invoice_date' ] = pdateparse( iltb.get_meta( invoice, 'invoice_date' ) )
		except ValueError:
			raise BusLogError( 'The invoice date is invalid' )

		try:
			if new_data[ 'due_date' ] is not None:
				new_data[ 'due_date' ] = pdateparse( new_data[ 'due_date' ] )
			else:
				new_data[ 'due_date' ] = pdateparse( iltb.get_meta( invoice, "due_date" ) )
		except ValueError:
			raise BusLogError( 'The due date is invalid' )

		if new_data[ 'due_date' ] < new_data[ 'invoice_date' ]:
			raise BusLogError( 'The due date is before the invoice date' )

	@staticmethod
	def _update_sanitize_state( invoice, new_data ):
		if new_data[ 'state' ] is not None:
			new_data['state'] = int( new_data.get( 'state' ) )
		else:
			new_data[ 'state' ] = invoice.document_state

		if ItemListState.get( new_data['state'] ) is None:
			raise BusLogError( 'Unknown new state requested for invoice.' )


	@staticmethod
	def _update_get_tax_rate( mystr ):
		val = TaxRate.get( long(mystr) )
		if val is None:
			raise BusLogError( 'The tax rate specified appears to be invalid' )
		return val[0]

	@staticmethod
	def _update_sanitize_items( invoice, new_data ):
		new_items = []
		for row in new_data[ 'items' ]:
			if len( row[0] ) > 0:
				try:
					row[1] = pnumparse( row[1] )
					row[2] = pnumparse( row[2] )
					row[3] = InvoiceBusLog._update_get_tax_rate( row[3] )
					row[4] = pnumparse( row[4] )
					if (row[1] >= 0) and (row[2] >= 0) and (row[4] >= 0):
						new_items.append( row )
				except:
					pass

		new_data[ 'items' ] = new_items
	

	@staticmethod
	def _update_sanitize_major_numbers( invoice, new_data ):
		try:
			new_data[ 'tax' ] = pnumparse( new_data['tax'] )
		except:
			new_data[ 'tax' ] = invoice.tax

		try:
			new_data[ 'amount' ] = pnumparse( new_data['amount'] )
		except:
			new_data[ 'amount' ] = invoice.amount

		try:
			new_data[ 'total' ] = pnumparse( new_data['total'] )
		except:
			new_data[ 'total' ] = invoice.total

	@staticmethod
	def _update_sanitize_item_numbers( invoice, new_data ):

		for pos, row in enumerate( new_data[ 'items' ] ):

			expected = row[1] * row[2] / 100
			received = row[4]

			if (received <= (expected - MarginsOfError.CURRENCY)) or (received >= (expected + MarginsOfError.CURRENCY)):
				raise BusLogError( 'Item row {} calculations did not stand up to scrutiny.'.format( pos ) )

	@staticmethod
	def _update_sanitize_tax_amounts( invoice, new_data ):

		sum_amount = 0
		sum_tax = 0
		sum_total = 0

		for row in new_data[ 'items' ]:

			my_product = row[1] * row[2] / 100

			temp_amount = 0
			temp_tax = 0
			temp_total = 0

			if row[3] == TaxRate.NONE or row[3] == TaxRate.EXEMPT:
				temp_amount = my_product
				temp_total = my_product

			if row[3] == TaxRate.EXCLUSIVE:
				# TODO: Dynamic tax rate
				temp_tax = long(my_product * 0.14)
				temp_amount = my_product
				temp_total = temp_amount + temp_tax

			if row[3] == TaxRate.INCLUSIVE:
				# TODO: Dynamic tax rate
				temp_amount = long(my_product / 1.14)
				temp_tax = my_product - temp_amount
				temp_total = my_product

			sum_amount += temp_amount
			sum_tax += temp_tax
			sum_total += temp_total


		if ( fabs(sum_total - new_data[ 'total' ]) > MarginsOfError.CURRENCY ) or ( fabs(sum_tax - new_data[ 'tax' ]) > MarginsOfError.CURRENCY ) or ( fabs(sum_amount - new_data[ 'amount' ]) > MarginsOfError.CURRENCY ):
			raise BusLogError( 'There is a discrepency in the tax, amount and total calculations which were received.' )



	@staticmethod
	def _update_sanitize( invoice, new_data ):
		InvoiceBusLog._update_sanitize_dates( invoice, new_data )
		InvoiceBusLog._update_sanitize_state( invoice, new_data )

		if invoice.document_state == ItemListState.DRAFT:
			InvoiceBusLog._update_sanitize_items( invoice, new_data )
			InvoiceBusLog._update_sanitize_major_numbers( invoice, new_data )
			InvoiceBusLog._update_sanitize_item_numbers( invoice, new_data )
			InvoiceBusLog._update_sanitize_tax_amounts( invoice, new_data )

		new_data[ 'comment' ] = new_data.get( 
								'comment',
								iltb.get_meta( invoice, 'comment', '' )
							)[:255]


	@staticmethod
	def _update_perform_update( invoice, new_data ):

		iltb.clear_meta( invoice )
		
		iltb.set_meta( invoice, 'invoice_date', pdate( new_data[ 'invoice_date' ] ) )
		iltb.set_meta( invoice, 'due_date', pdate( new_data[ 'due_date' ] ) )
		iltb.set_meta( invoice, 'comment', new_data[ 'comment' ] )

		if invoice.document_state == ItemListState.DRAFT:

			iltb.clear_lines( invoice )

			for row in new_data[ 'items' ]:
				il = iltb.add_line(
						invoice,
						description = row[0],
						units = row[1],
						perunit = row[2],
						tax_rate = row[3]
					)


	@staticmethod
	def _update_finalize_invoice( invoice ):
		transaction = AccountBusLog.adjust(
				invoice.client.account,
				'INVOICE',
				'Invoice {}'.format( invoice.refnum ),
				float(0)-invoice.total,
				ObjRoute.gen( invoice ),
				''
			)


	@staticmethod
	def _update_void_invoice( invoice ):
		transaction = AccountBusLog.adjust(
				invoice.client.account,
				'VOID',
				'Void of Invoice {}'.format( invoice.refnum ),
				invoice.total,
				ObjRoute.gen( invoice ),
				''
			)



	@staticmethod
	def _update_handle_state_change( invoice, new_data ):
		ns = new_data['state']

		if invoice.document_state == ns:
			return

		if invoice.document_state == ItemListState.DRAFT:
			if ns != ItemListState.FINAL:
				raise BusLogError( 'You can only finalize this invoice' )
			invoice.document_state = ns
			InvoiceBusLog._update_finalize_invoice( invoice )
			return

		if invoice.document_state == ItemListState.FINAL:
			if ns != ItemListState.VOID:
				raise BusLogError( 'You can only void this invoice' )
			invoice.document_state = ns
			InvoiceBusLog._update_void_invoice( invoice )
			return


	@staticmethod
	def update( invoice, new_data ):
		
		my_new_data = deepcopy( new_data )

		InvoiceBusLog._update_sanitize( invoice, my_new_data )
		InvoiceBusLog._update_perform_update( invoice, my_new_data )
		InvoiceBusLog._update_handle_state_change( invoice, my_new_data )
		invoice.save()


