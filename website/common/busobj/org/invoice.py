from __future__ import unicode_literals

from common.models import *
from common.exceptions import *
from common.utils.dbgdatetime import datetime
from common.utils.parse import *

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


