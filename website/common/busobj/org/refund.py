from __future__ import unicode_literals

from common.models import *
from common.exceptions import *
from common.utils.dbgdatetime import datetime
from common.utils.parse import *

from source_document import SourceDocumentObj



class RefundObj( SourceDocumentObj ):

	def __init__( self, sdid = None ):
		super( RefundObj, self ).__init__( sdid )

	def initialize( self, source_document, amount, refund_date ):
		super( RefundObj, self ).initialize(
				source_document.getObj().client,
				SourceDocumentType.REFUND,
				SourceDocumentState.FINAL
			)

		specs = self.getSpecs()
		specs.setRefundDate( refund_date )
		specs.setComment( "" )
		return self

	

	def getSpecs( self ):
		class Specifics( object ):
			def __init__( self, parent ):
				self.parent = parent
				
			def getRefundDate( self ):
				return pdateparse( self.parent.getMeta().get( "refund_date" ) )

			def setRefundDate( self, date ):
				self.parent.getMeta().set( "refund_date", pdate( date ) )

			def getComment( self ):
				return self.parent.getMeta().get( "comment" )

			def setComment( self, comment ):
				self.parent.getMeta().set( "comment", comment[:255] )

		return Specifics( self )


