from __future__ import unicode_literals

from common.models import *
from common.exceptions import *
from common.utils.dbgdatetime import datetime
from common.utils.parse import *

from common.buslog.org import AccountBusLog

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

		self.getLines().add(
			'Refund from {}'.format( source_document.getObj().refnum ),
			100,
			amount,
			TaxRate.NONE
		)

		self.getActions().apply()

		self.getAllocations().receive( source_document, amount )
		return self

	
	def getActions( self ):
		class Actions( object ):
			def __init__( self, parent ):
				self.parent = parent

			def apply( self ):
				AccountBusLog.adjust(
					self.parent.getObj().client.account,
					self.parent.getSpecs().getRefundDate(),
					'REFUND',
					'Refund {}'.format( self.parent.getObj().refnum ),
					((float(0) - self.parent.getTotals().getTotal())),
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
					self.parent.getSpecs().getRefundDate(),
					'VOID',
					'Void of Refund {}'.format( self.parent.getObj().refnum ),
					(self.parent.getTotals().getTotal()),
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
				
			def getRefundDate( self ):
				return pdateparse( self.parent.getMeta().get( "refund_date" ) )

			def setRefundDate( self, date ):
				self.parent.getMeta().set( "refund_date", pdate( date ) )

			def getComment( self ):
				return self.parent.getMeta().get( "comment" )

			def setComment( self, comment ):
				self.parent.getMeta().set( "comment", comment[:255] )

		return Specifics( self )


