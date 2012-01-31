from __future__ import unicode_literals

from math import *
from copy import deepcopy

from common.models import *
from common.exceptions import *
from common.buslog.org import AccountBusLog
from common.busobj.org import InvoiceObj
from common.moe import MarginsOfError
from common.utils.dbgdatetime import datetime
from common.utils.parse import *



from common.bushelp.org.actions import ActionFactory
from common.bushelp.org.allocator import Allocator

# Helper
#	
#



class InvoiceHelper( object ):



	@staticmethod
	def _update_sanitize_dates( inv, new_data ):
		try:
			if new_data[ 'invoice_date' ] is not None:
				new_data[ 'invoice_date' ] = pdateparse( new_data[ 'invoice_date' ] )
			else:
				new_data[ 'invoice_date' ] = inv.getSpecs().getInvoiceDate()
		except ValueError:
			raise BusLogError( 'The invoice date is invalid' )

		try:
			if new_data[ 'due_date' ] is not None:
				new_data[ 'due_date' ] = pdateparse( new_data[ 'due_date' ] )
			else:
				new_data[ 'due_date' ] = inv.getSpecs().getDueDate()
		except ValueError:
			raise BusLogError( 'The due date is invalid' )

		if new_data[ 'due_date' ] < new_data[ 'invoice_date' ]:
			raise BusLogError( 'The due date is before the invoice date' )

	@staticmethod
	def _update_sanitize_state( inv, new_data ):
		if new_data[ 'state' ] is not None:
			new_data['state'] = int( new_data.get( 'state' ) )
		else:
			new_data[ 'state' ] = inv.getObj().document_state

		if SourceDocumentState.get( new_data['state'] ) is None:
			raise BusLogError( 'Unknown new state requested for invoice.' )


	@staticmethod
	def _update_get_tax_rate( mystr ):
		val = TaxRate.get( long(mystr) )
		if val is None:
			raise BusLogError( 'The tax rate specified appears to be invalid' )
		return val[0]

	@staticmethod
	def _update_sanitize_items( inv, new_data ):
		new_items = []

		try:
			for row in new_data[ 'items' ]:
				if len( row[0] ) > 0:
					try:
						row[1] = pnumparse( row[1] )
						row[2] = pnumparse( row[2] )
						row[3] = InvoiceHelper._update_get_tax_rate( row[3] )
						if (row[1] >= 0) and (row[2] >= 0):
							new_items.append( row )
					except KeyError:
						pass
		except KeyError:
			pass

		new_data[ 'items' ] = new_items

	@staticmethod
	def _update_sanitize( inv, new_data ):
		InvoiceHelper._update_sanitize_dates( inv, new_data )
		InvoiceHelper._update_sanitize_state( inv, new_data )

		if inv.getObj().document_state == SourceDocumentState.DRAFT:
			InvoiceHelper._update_sanitize_items( inv, new_data )

		new_data[ 'comment' ] = new_data.get( 
								'comment',
								inv.getSpecs().getComment()
							)[:255]


	@staticmethod
	def _update_perform_update( inv, new_data ):

		inv.getSpecs().setInvoiceDate( new_data[ 'invoice_date' ] )
		inv.getSpecs().setDueDate( new_data[ 'due_date' ] )
		inv.getSpecs().setComment( new_data[ 'comment' ] )


		if inv.getObj().document_state == SourceDocumentState.DRAFT:

			inv.getLines().clear()

			for row in new_data[ 'items' ]:
				il = inv.getLines().add(
						description = row[0],
						units = row[1],
						perunit = row[2],
						tax_rate = row[3]
					)


	@staticmethod
	def _update_handle_state_change( obj, new_data ):
		try:
			ns = new_data['state']
		except KeyError:
			return

		if ns == obj.getObj().document_state:
			return

		af = ActionFactory.instantiate( obj )

		if ns == SourceDocumentState.FINAL:
			af.finalize()
			return

		if ns == SourceDocumentState.VOID:
			ally = Allocator( af )
			ally.clear()
			af.void()
			return

		if ns == SourceDocumentState.DELETE:
			af.delete()
			return

		raise BusLogError( 'Invalid state change requested.' )


	@staticmethod
	def update( invoice, new_data ):
		
		my_new_data = deepcopy( new_data )

		inv = InvoiceObj()
		inv.wrap( invoice )

		InvoiceHelper._update_sanitize( inv, my_new_data )
		InvoiceHelper._update_perform_update( inv, my_new_data )
		InvoiceHelper._update_handle_state_change( inv, my_new_data )


