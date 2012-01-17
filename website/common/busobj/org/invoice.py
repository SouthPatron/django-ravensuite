from __future__ import unicode_literals

from common.models import *
from common.exceptions import *
from common.utils.dbgdatetime import datetime
from common.utils.objroute import *
from common.utils.parse import *

from source_document import SourceDocumentObj


class InvoiceObj( object ):

	@staticmethod
	def create( client ):
		sdo = SourceDocumentObj.create(
				client,
				SourceDocumentType.INVOICE,
				SourceDocumentState.DRAFT
			)

		tmpobj = InvoiceObj( sdid = None )
		tmpobj.sdo = sdo
		tmpobj.setInvoiceDate( datetime.date.today() )
		tmpobj.setDueDate( datetime.date.today() + datetime.timedelta( weeks = 4 ) )
		tmpobj.setComment( "" )
		return tmpobj


	def __init__( self, sdid ):
		if sdid is not None:
			self.sdo = SourceDocument( sdid = sdid )



	def getInvoiceDate( self ):
		return pdateparse( self.sdo.get_meta( "invoice_date" ) )

	def setInvoiceDate( self, date ):
		self.sdo.set_meta( "invoice_date", pdate( date ) )

	def getDueDate( self ):
		return pdateparse( self.sdo.get_meta( "due_date" ) )

	def setDueDate( self, date ):
		self.sdo.set_meta( "due_date", pdate( date ) )

	def getComment( self ):
		return self.sdo.get_meta( "comment" )

	def setComment( self, comment ):
		self.sdo.set_meta( "comment", comment[:255] )

	def getAmount( self ):
		return self.sdo.getAmount()

	def setAmount( self, amount ):
		return self.sdo.setAmount( amount )

	def getTax( self ):
		return self.sdo.getTax()

	def setTax( self, tax ):
		return self.sdo.setTax( tax )

	def getTotal( self ):
		return self.sdo.getTotal()

	def setTotal( self, total ):
		return self.sdo.setTotal( total )

	def getLines( self ):
		for line in self.sdo.get_lines( self.sdo ):
			yield { 
				"description" : line.description,
				"units" : line.units,
				"perunit" : line.perunit,
				"amount" : line.amount,
				"tax_rate" : TaxRate.get( line.tax_rate )[0],
				"tax_display" : TaxRate.get( line.tax_rate )[1],
				"tax_amount" : line.tax_amount,
				"total" : line.total
			}

	def addLine( self, description, units, perunit, tax_rate ):
		line = self.sdo.add_line( description, units, perunit, tax_rate )
		self.sdo.sdo.amount += line.amount
		self.sdo.sdo.tax += line.tax_amount
		self.sdo.sdo.total += line.total


	def save( self ):
		self.sdo.save()

	def get_single_url( self ):
		return self.sdo.sdo.get_single_url()
	

