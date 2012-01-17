from __future__ import unicode_literals

from math import *
from copy import deepcopy

from common.models import *
from common.exceptions import *
from common.buslog.org import AccountBusLog
from common.moe import MarginsOfError
from common.utils.dbgdatetime import datetime
from common.utils.objroute import *
from common.utils.parse import *


class SourceDocumentObj( object ):

	@staticmethod
	def create( client, document_type, document_state ):

		# TODO: select_for_update()
		sc = OrganizationCounter.objects.get( organization__refnum = client.org.refnum )
		refnum = sc.source_document_no
		sc.source_document_no += 1
		sc.save()

		sdo = SourceDocument()
		sdo.refnum = refnum
		sdo.client = client
		sdo.document_type = document_type
		sdo.document_state = document_state
		sdo.creation_time = datetime.datetime.now()
		sdo.save()

		tmpobj = SourceDocumentObj( sdid = None )
		tmpobj.sdo = sdo
		return tmpobj


	def __init__( self, sdid ):
		if sdid is not None:
			self.sdo = SourceDocument.objects.get( refnum = sdid )
			

	def delete( self ):
		self.sdo.delete()

	def	set_meta( self, key, value ):

		sam = None

		rc = SourceDocumentMeta.objects.filter(
				source_document = self.sdo,
				key = key
			)
		if rc.count() == 0:
			sam = SourceDocumentMeta( source_document = self.sdo, key = key )
		else:
			sam = rc[0]

		sam.value = '{}'.format( value )
		sam.save()


	def get_meta( self, key, default = None ):
		rc = SourceDocumentMeta.objects.filter(
				source_document = self.sdo,
				key = key
			)
		if rc.count() <= 0:
			if default is not None:
				return default
			raise RuntimeError( 'No results found' )

		return rc[0].value
	
	def clear_meta( self, key = None ):
		if key is None:
			SourceDocumentMeta.objects.filter( source_document = self.sdo ).delete()
		else:
			SourceDocumentMeta.objects.filter( source_document = self.sdo, key = key ).delete()

	def get_all_meta( self ):
		return SourceDocumentMeta.objects.filter( source_document = self.sdo )


	def add_line( self, description, units, perunit, tax_rate ):

		my_total = 0
		my_tax = 0
		my_amount = 0
		# TODO: dynamic tax rate
		my_tax_rate = 0.14

		multiple = long( units * perunit / 100 )

		if tax_rate == TaxRate.NONE or tax_rate == TaxRate.EXEMPT:
			my_amount = multiple
			my_tax = 0
			my_total = multiple
		elif tax_rate == TaxRate.EXCLUSIVE:
			my_tax = long( multiple * my_tax_rate )
			my_total = multiple + my_tax
			my_amount = multiple
		elif tax_rate == TaxRate.INCLUSIVE:
			my_total = multiple
			my_tax = multiple - long(long( multiple * 100 / (1 + my_tax_rate) ) / 100)
			my_amount = my_total - my_tax


		sam = SourceDocumentLine(
				source_document = self.sdo,
				description = description,
				units = units,
				perunit = perunit,
				amount = my_amount,
				tax_rate = tax_rate,
				tax_amount = my_tax,
				total = my_total
			)
		sam.save()

		return sam

	
	def clear_lines( self ):
		SourceDocumentLine.objects.filter( source_document = self.sdo ).delete()
		self.sdo.save()

	def get_lines( self ):
		return SourceDocumentLine.objects.filter( source_document = self.sdo )

	def getTotal( self ):
		return self.sdo.total

	def setTotal( self, total ):
		self.sdo.total = total
	
	def getAmount( self ):
		return self.sdo.amount

	def setAmount( self, amount ):
		self.sdo.amount = self.sdo.amount
	
	def getTax( self ):
		return self.sdo.tax

	def setTax( self, tax ):
		self.sdo.tax = tax

	def save( self ):
		self.sdo.save()



