from __future__ import unicode_literals

from common.models import *
from common.exceptions import *
from common.utils.dbgdatetime import datetime
from common.utils.parse import *

from common.buslog.org import AccountBusLog

from source_document import SourceDocumentObj



class InvoiceObj( SourceDocumentObj ):

	def __init__( self, sdid = None ):
		super( InvoiceObj, self ).__init__( sdid )

	def initialize( self, client ):
		super( InvoiceObj, self ).initialize(
				client,
				SourceDocumentType.INVOICE,
				SourceDocumentState.DRAFT
			)

		specs = self.getSpecs()

		specs.setInvoiceDate( datetime.date.today() )
		specs.setDueDate( datetime.date.today() + datetime.timedelta( weeks = 4 ) )
		specs.setComment( "" )
		return self

	
	def getActions( self ):
		class Actions( object ):
			def __init__( self, parent ):
				self.parent = parent

			def delete( self ):
				if self.parent.getObj().document_state == SourceDocumentState.FINAL:
					raise BusLogError( 'This invoice has already been finalized. Try voiding it instead.' )
				if self.parent.getObj().document_state == SourceDocumentState.VOID:
					raise BusLogError( 'This invoice has already been voided. It can not be removed.' )

				self.parent.delete()

			def finalize( self ):
				ns = self.parent.getObj().document_state

				if ns != SourceDocumentState.DRAFT:
					raise BusLogError( 'This invoice can not be finalized because it is not a draft.' )

				self.parent.getObj().document_state = SourceDocumentState.FINAL
				self.parent.save()

				AccountBusLog.adjust(
					self.parent.getObj().client.account,
					self.parent.getSpecs().getInvoiceDate(),
					'INVOICE',
					'Invoice {}'.format( self.parent.getObj().refnum ),
					long(0) - (self.parent.getTotals().getTotal()),
					self.parent.getObj(),
					''
				)

			def void( self ):

				ns = self.parent.getObj().document_state

				if ns != SourceDocumentState.FINAL:
					raise BusLogError( 'This invoice can not be voided because it is not yet finalized.' )

				self.parent.getObj().document_state = SourceDocumentState.VOID
				self.parent.save()

				AccountBusLog.adjust(
					self.parent.getObj().client.account,
					self.parent.getSpecs().getInvoiceDate(),
					'VOID',
					'Void of Invoice {}'.format( self.parent.getObj().refnum ),
					(self.parent.getTotals().getTotal()),
					self.parent.getObj(),
					''
				)

				return

		return Actions( self )



	def getSpecs( self ):
		class Specifics( object ):
			def __init__( self, parent ):
				self.parent = parent
				
			def getInvoiceDate( self ):
				return pdateparse( self.parent.getMeta().get( "invoice_date" ) )

			def setInvoiceDate( self, date ):
				self.parent.getMeta().set( "invoice_date", pdate( date ) )

			def getDueDate( self ):
				return pdateparse( self.parent.getMeta().get( "due_date" ) )

			def setDueDate( self, date ):
				self.parent.getMeta().set( "due_date", pdate( date ) )

			def getComment( self ):
				return self.parent.getMeta().get( "comment" )

			def setComment( self, comment ):
				self.parent.getMeta().set( "comment", comment[:255] )

		return Specifics( self )


