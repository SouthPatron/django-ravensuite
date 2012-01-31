from __future__ import unicode_literals

from common.models import *
from common.exceptions import *
from common.utils.dbgdatetime import datetime
from common.utils.parse import *

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

