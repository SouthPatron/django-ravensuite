from __future__ import unicode_literals

from math import *

from common.models import *
from common.exceptions import *
from common.buslog.org import AccountBusLog
from common.moe import MarginsOfError
from common.utils.dbgdatetime import datetime


class InvoiceBusLog( object ):

	@staticmethod
	def get_next_refnum( org ):
		# TODO: select_for_update()
		sc = OrganizationCounter.objects.get( organization__refnum = org.refnum )
		refnum = sc.invoice_no
		sc.invoice_no += 1
		sc.save()
		return refnum


	@staticmethod
	def create( client ):

		if ( account.is_enabled is False ):
			raise BusLogError( 'The account against which the invoice is being raised is not enabled.' )

		newt = Invoice()
		newt.account = account
		newt.refnum = InvoiceBusLog.get_next_refnum( account.get_org() )
		newt.creation_time = datetime.datetime.now()
		newt.invoice_date = datetime.date.today()
		newt.due_date = datetime.date.today() + datetime.timedelta( weeks = 4 )
		newt.amount = 0
		newt.tax = 0
		newt.total = 0
		newt.comment = ""
		newt.is_paid = False
		newt.state = InvoiceState.DRAFT
		newt.save()
		return newt

	@staticmethod
	def delete( invoice ):
		if invoice.state == InvoiceState.FINAL:
			raise BusLogError( 'This invoice has already been finalized. Try voiding it instead.' )
		if invoice.state == InvoiceState.VOID:
			raise BusLogError( 'This invoice has already been voided. It can not be removed.' )
		invoice.delete()


	@staticmethod
	def _update_sanitize_dates( new_data ):
		try:
			new_data[ 'invoice_date' ] = datetime.datetime.strptime( new_data[ 'invoice_date' ], '%d %b %Y' )
		except ValueError:
			raise BusLogError( 'The invoice date is invalid' )

		try:
			new_data[ 'due_date' ] = datetime.datetime.strptime( new_data[ 'due_date' ], '%d %b %Y' )
		except ValueError:
			raise BusLogError( 'The due date is invalid' )

		if new_data[ 'due_date' ] < new_data[ 'invoice_date' ]:
			raise BusLogError( 'The due date is before the invoice date' )

	@staticmethod
	def _update_sanitize_state( new_data ):
		new_data['state'] = int(new_data['state'])
		if InvoiceState.get( new_data['state'] ) is None:
			raise BusLogError( 'Unknown new state requested for invoice.' )


	@staticmethod
	def _update_get_tax_rate( mystr ):
		val = TaxRate.get_by_display( mystr )
		if val is None:
			raise BusLogError( 'The tax rate specified appears to be invalid' )
		return val[0]

	@staticmethod
	def _update_sanitize_items( new_data ):
		new_items = []
		for row in new_data[ 'items' ]:
			if len( row[0] ) > 0:
				try:
					row[1] = long(float(row[1]) * 100)
					row[2] = long(float(row[2]) * 100)
					row[3] = InvoiceBusLog._update_get_tax_rate( row[3] )
					row[4] = long(float(row[4]) * 100)

					if (row[1] >= 0) and (row[2] >= 0) and (row[4] >= 0):
						new_items.append( row )
				except:
					pass
		new_data[ 'items' ] = new_items
	

	@staticmethod
	def _update_sanitize_major_numbers( new_data ):
		new_data[ 'tax' ] = long(float(new_data['tax']) * 100)
		new_data[ 'amount' ] = long(float(new_data['amount']) * 100)
		new_data[ 'total' ] = long(float(new_data['total']) * 100)

	@staticmethod
	def _update_sanitize_item_numbers( new_data ):

		for pos, row in enumerate( new_data[ 'items' ] ):

			expected = row[1] * row[2] / 100
			received = row[4]

			if (received <= (expected - MarginsOfError.CURRENCY)) or (received >= (expected + MarginsOfError.CURRENCY)):
				raise BusLogError( 'Item row {} calculations did not stand up to scrutiny.'.format( pos ) )

	@staticmethod
	def _update_sanitize_tax_amounts( new_data ):

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
	def _update_sanitize( new_data ):
		InvoiceBusLog._update_sanitize_dates( new_data )
		InvoiceBusLog._update_sanitize_state( new_data )
		InvoiceBusLog._update_sanitize_items( new_data )
		InvoiceBusLog._update_sanitize_major_numbers( new_data )
		InvoiceBusLog._update_sanitize_item_numbers( new_data )
		InvoiceBusLog._update_sanitize_tax_amounts( new_data )

		new_data["comment"] = new_data["comment"][:255]


	@staticmethod
	def _update_perform_update( invoice, new_data ):
		invoice.invoice_date = new_data[ 'invoice_date' ]
		invoice.due_date = new_data[ 'due_date' ]
		invoice.comment = new_data[ 'comment' ]

		if invoice.state == InvoiceState.DRAFT:
			invoice.amount = new_data[ 'amount' ]
			invoice.tax = new_data[ 'tax' ] 
			invoice.total = new_data[ 'total' ]

			InvoiceLine.objects.filter( invoice = invoice ).delete()

			for row in new_data[ 'items' ]:
				il = InvoiceLine.objects.create( invoice = invoice, description = row[0], units = row[1], perunit = row[2], tax_rate = row[3], total = row[4] )


	@staticmethod
	def _update_finalize_invoice( invoice ):
		transaction = AccountBusLog.adjust(
				invoice.account,
				'INVOICE',
				'Invoice {}'.format( invoice.refnum ),
				float(0)-invoice.total,
				''
			)


	@staticmethod
	def _update_void_invoice( invoice ):
		transaction = AccountBusLog.adjust(
				invoice.account,
				'VOID',
				'Void of Invoice {}'.format( invoice.refnum ),
				invoice.total,
				''
			)

	@staticmethod
	def _update_handle_state_change( invoice, new_data ):
		ns = new_data['state']

		if invoice.state == ns:
			return

		if invoice.state == InvoiceState.DRAFT:
			if ns != InvoiceState.FINAL:
				raise BusLogError( 'You can only finalize this invoice' )
			invoice.state = ns
			InvoiceBusLog._update_finalize_invoice( invoice )
			return

		if invoice.state == InvoiceState.FINAL:
			if ns != InvoiceState.VOID:
				raise BusLogError( 'You can only void this invoice' )
			invoice.state = ns
			InvoiceBusLog._update_void_invoice( invoice )
			return


	@staticmethod
	def update( invoice, new_data ):
		InvoiceBusLog._update_sanitize( new_data )
		InvoiceBusLog._update_perform_update( invoice, new_data )
		InvoiceBusLog._update_handle_state_change( invoice, new_data )
		invoice.save()


