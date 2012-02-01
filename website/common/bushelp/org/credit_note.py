from __future__ import unicode_literals
from django.utils.translation import ugettext as _

from math import *
from copy import deepcopy

from common.models import *
from common.exceptions import *
from common.buslog.org import AccountBusLog
from common.busobj.org import CreditNoteObj
from common.moe import MarginsOfError
from common.utils.dbgdatetime import datetime
from common.utils.parse import *

from common.bushelp.org.actions import ActionFactory
from common.bushelp.org.allocator import Allocator


# Helper
#	
#



class CreditNoteHelper( object ):

	@staticmethod
	def _update_sanitize_dates( crd, new_data ):
		try:
			if new_data[ 'credit_note_date' ] is not None:
				new_data[ 'credit_note_date' ] = pdateparse( new_data[ 'credit_note_date' ] )
			else:
				new_data[ 'credit_note_date' ] = crd.getSpecs().getCreditNoteDate()
		except ValueError:
			raise BLE_InvalidInputError( _('BLE_10001') )


	@staticmethod
	def _update_sanitize_state( crd, new_data ):
		if new_data[ 'state' ] is not None:
			new_data['state'] = int( new_data.get( 'state' ) )
		else:
			new_data[ 'state' ] = crd.getObj().document_state

		if SourceDocumentState.get( new_data['state'] ) is None:
			raise BLE_InvalidInputError( _('BLE_10002') )


	@staticmethod
	def _update_get_tax_rate( mystr ):
		val = TaxRate.get( long(mystr) )
		if val is None:
			raise BLE_InvalidInputError( _('BLE_10401') )
		return val[0]

	@staticmethod
	def _update_sanitize_items( crd, new_data ):
		new_items = []

		try:
			for row in new_data[ 'items' ]:
				if len( row[0] ) > 0:
					try:
						row[1] = pnumparse( row[1] )
						row[2] = pnumparse( row[2] )
						row[3] = CreditNoteHelper._update_get_tax_rate( row[3] )
						if (row[1] >= 0) and (row[2] >= 0):
							new_items.append( row )
					except KeyError:
						pass
		except KeyError:
			pass

		new_data[ 'items' ] = new_items

	@staticmethod
	def _update_sanitize( crd, new_data ):
		CreditNoteHelper._update_sanitize_dates( crd, new_data )
		CreditNoteHelper._update_sanitize_state( crd, new_data )

		if crd.getObj().document_state == SourceDocumentState.DRAFT:
			CreditNoteHelper._update_sanitize_items( crd, new_data )

		new_data[ 'comment' ] = new_data.get( 
								'comment',
								crd.getSpecs().getComment()
							)[:255]


	@staticmethod
	def _update_perform_update( crd, new_data ):

		crd.getSpecs().setCreditNoteDate( new_data[ 'credit_note_date' ] )
		crd.getSpecs().setComment( new_data[ 'comment' ] )


		if crd.getObj().document_state == SourceDocumentState.DRAFT:

			crd.getLines().clear()

			for row in new_data[ 'items' ]:
				il = crd.getLines().add(
						description = row[0],
						units = row[1],
						perunit = row[2],
						tax_rate = row[3]
					)


	@staticmethod
	def _update_handle_state_change( crd, new_data ):
		try:
			ns = new_data['state']
		except KeyError:
			return

		if ns == crd.getObj().document_state:
			return

		af = ActionFactory.instantiate( crd )

		if ns == SourceDocumentState.FINAL:
			af.finalize()
			return

		if ns == SourceDocumentState.VOID:
			ally = Allocator()
			ally.clear( crd )
			af.void()
			return

		if ns == SourceDocumentState.DELETE:
			af.delete()
			return

		raise BLE_InvalidInputError( _('BLE_10402') )


	@staticmethod
	def update( credit_note, new_data ):
		
		my_new_data = deepcopy( new_data )

		crd = CreditNoteObj()
		crd.wrap( credit_note )

		CreditNoteHelper._update_sanitize( crd, my_new_data )
		CreditNoteHelper._update_perform_update( crd, my_new_data )
		CreditNoteHelper._update_handle_state_change( crd, my_new_data )


