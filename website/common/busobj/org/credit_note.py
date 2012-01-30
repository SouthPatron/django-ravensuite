from __future__ import unicode_literals

from common.models import *
from common.exceptions import *
from common.utils.dbgdatetime import datetime
from common.utils.parse import *

from common.buslog.org import AccountBusLog

from source_document import SourceDocumentObj



class CreditNoteObj( SourceDocumentObj ):

	def __init__( self, sdid = None ):
		super( CreditNoteObj, self ).__init__( sdid )

	def initialize( self, client ):
		super( CreditNoteObj, self ).initialize(
				client,
				SourceDocumentType.CREDIT_NOTE,
				SourceDocumentState.DRAFT
			)

		specs = self.getSpecs()
		specs.setCreditNoteDate( datetime.date.today() )
		specs.setComment( "" )
		return self
	
	def getActions( self ):
		class Actions( object ):
			def __init__( self, parent ):
				self.parent = parent

			def delete( self ):
				if self.parent.getObj().document_state == SourceDocumentState.FINAL:
					raise BusLogError( 'This credit note has already been finalized. Try voiding it instead.' )
				if self.parent.getObj().document_state == SourceDocumentState.VOID:
					raise BusLogError( 'This credit note has already been voided. It can not be removed.' )

				self.parent.delete()

			def finalize( self ):
				ns = self.parent.getObj().document_state

				if ns != SourceDocumentState.DRAFT:
					raise BusLogError( 'This credit note can not be finalized because it is not a draft.' )

				self.parent.getObj().document_state = SourceDocumentState.FINAL
				self.parent.save()

				AccountBusLog.adjust(
					self.parent.getObj().client.account,
					self.parent.getSpecs().getCreditNoteDate(),
					'CREDIT NOTE',
					'CreditNote {}'.format( self.parent.getObj().refnum ),
					(self.parent.getTotals().getTotal()),
					self.parent.getObj(),
					''
				)

			def void( self ):

				ns = self.parent.getObj().document_state

				if ns != SourceDocumentState.FINAL:
					raise BusLogError( 'This credit note can not be voided because it is not yet finalized.' )

				self.parent.getObj().document_state = SourceDocumentState.VOID
				self.parent.save()

				AccountBusLog.adjust(
					self.parent.getObj().client.account,
					self.parent.getSpecs().getCreditNoteDate(),
					'VOID',
					'Void of CreditNote {}'.format( self.parent.getObj().refnum ),
					(long(0) - (self.parent.getTotals().getTotal())),
					self.parent.getObj(),
					''
				)

				self.parent.getAllocations().clear()
				return

		return Actions( self )

	def getSpecs( self ):
		class Specifics( object ):
			def __init__( self, parent ):
				self.parent = parent
				
			def getCreditNoteDate( self ):
				return pdateparse( self.parent.getMeta().get( "credit_note_date" ) )

			def setCreditNoteDate( self, date ):
				self.parent.getMeta().set( "credit_note_date", pdate( date ) )

			def getComment( self ):
				return self.parent.getMeta().get( "comment" )

			def setComment( self, comment ):
				self.parent.getMeta().set( "comment", comment[:255] )

		return Specifics( self )

