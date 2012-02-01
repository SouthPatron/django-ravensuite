from __future__ import unicode_literals

from common.models import *
from common.exceptions import *
from common.utils.dbgdatetime import datetime
from common.utils.parse import *

from source_document import SourceDocumentObj



class RefundObj( SourceDocumentObj ):

	def __init__( self, sdid = None ):
		super( RefundObj, self ).__init__( sdid )

	def initialize( self, client ):
		super( RefundObj, self ).initialize(
				client,
				SourceDocumentType.REFUND,
				SourceDocumentState.DRAFT
			)

		specs = self.getSpecs()
		specs.setRefundDate( datetime.datetime.now() )
		specs.setComment( "" )
		return self

	

	def getSpecs( self ):
		class Specifics( object ):
			def __init__( self, parent ):
				self.parent = parent
				
			def getRefundDate( self ):
				return self.parent.getDates().getEventTime()

			def setRefundDate( self, dat ):
				self.parent.getDates().setEventTime( dat )

			def getComment( self ):
				return self.parent.getMeta().get( "comment" )

			def setComment( self, comment ):
				self.parent.getMeta().set( "comment", comment[:255] )

		return Specifics( self )


