from __future__ import unicode_literals

from django.db.models import Q
from common.models import *
from common.exceptions import *
from common.utils.dbgdatetime import datetime
from common.utils.parse import *


class SourceDocumentObj( object ):

	def __init__( self, sdid = None ):
		self.sdo = None
		if sdid is not None:
			self.load( sdid )
	
	def initialize( self, client, document_type, document_state ):

		# TODO: select_for_update()
		sc = OrganizationCounter.objects.get( organization__refnum = client.get_org().refnum )
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

		self.sdo = sdo
		return self

	def getObj( self ):
		return self.sdo
	
	def load( self, sdid ):
		self.sdo = SourceDocument.objects.get( refnum = sdid )
	
	def wrap( self, sdo ):
		self.sdo = sdo

	def delete( self ):
		self.getAllocations().clear()
		self.sdo.delete()

	def save( self ):
		self.sdo.save()

	def get_single_url( self ):
		return self.sdo.get_single_url()


	class Lines( object ):
		def __init__( self, parent ):
			self.parent = parent

		def add( self, description, units, perunit, tax_rate ):
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
					source_document = self.parent.getObj(),
					description = description,
					units = units,
					perunit = perunit,
					amount = my_amount,
					tax_rate = tax_rate,
					tax_amount = my_tax,
					total = my_total
				)
			sam.save()

			if my_amount != 0 and my_total != 0:
				self.parent.getObj().total += my_total
				self.parent.getObj().tax += my_tax
				self.parent.getObj().amount += my_amount
				self.parent.save()

			return sam


		def clear( self ):
			objs = SourceDocumentLine.objects.filter( source_document = self.parent.getObj() )
			if objs.count() > 0:
				objs.delete()
				self.parent.getObj().total = 0
				self.parent.getObj().tax = 0
				self.parent.getObj().amount = 0
				self.parent.save()


		def all( self ):
			return SourceDocumentLine.objects.filter( source_document = self.parent.getObj() )


	def getLines( self ):
		return self.Lines( self )


	class Meta( object ):
		def __init__( self, parent ):
			self.parent = parent
		
		def	set( self, key, value ):
			sam = None
			isNew = False

			try:
				sam = SourceDocumentMeta.objects.get(
						source_document = self.parent.getObj(),
						key = key
					)
			except SourceDocumentMeta.DoesNotExist:
				sam = SourceDocumentMeta( source_document = self.parent.getObj(), key = key )
				isNew = True

			newval = '{}'.format( value )

			if isNew is True or newval != sam.value:
				sam.value = newval
				sam.save()


		def get( self, key ):
			rc = SourceDocumentMeta.objects.get(
					source_document = self.parent.getObj(),
					key = key
				)
			return rc.value

		def clear( self, key = None ):
			if key is None:
				SourceDocumentMeta.objects.filter( source_document = self.parent.getObj() ).delete()
			else:
				SourceDocumentMeta.objects.filter( source_document = self.parent.getObj(), key = key ).delete()

		def all( self ):
			return SourceDocumentMeta.objects.filter( source_document = self.parent.getObj() )


	def getMeta( self ):
		return self.Meta( self )


	class Totals( object ):
		def __init__( self, parent ):
			self.parent = parent

		def getTotal( self ):
			return self.parent.getObj().total

		def getAmount( self ):
			return self.parent.getObj().amount

		def getTax( self ):
			return self.parent.getObj().tax

		def getAllocated( self ):
			return self.parent.getObj().allocated

		def getUnallocated( self ):
			return self.getTotal() - self.getAllocated()

	def getTotals( self ):
		return self.Totals( self )


	class Allocations( object ):
		def __init__( self, parent ):
			self.parent = parent

		def all( self ):
			return SourceDocumentAllocation.objects.filter(
					Q( source = self.parent.getObj() ) | Q( destination = self.parent.getObj() )
				)

		def clear_one( self, sda, save_parent = True, myObj = None ):
		
			if myObj is None:
				myObj = self.parent.getObj()

			if sda.destination.id != myObj.id:
				sda.destination.allocated -= sda.amount
				sda.destination.save()
			else:
				myObj.allocated -= sda.amount

			if sda.source.id != myObj.id:
				sda.source.allocated -= sda.amount
				sda.source.save()
			else:
				myObj.allocated -= sda.amount

			sda.delete()

			if save_parent is True:
				self.parent.save()

		def clear_by_id( self, sda_id ):
			try:
				sda = SourceDocumentAllocation.objects.get(
						Q( source = self.parent.getObj() ) | Q( destination = self.parent.getObj() ),
						id = sda_id
					)
				return self.clear_one( sda )
			except SourceDocumentAllocation.DoesNotExist:
				raise BusLogError( 'There was no such allocation with that ID' )


		def clear( self ):
			myObj = self.parent.getObj()

			if myObj.document_state == SourceDocumentState.DRAFT:
				return

			for sda in self.all():
				self.clear_one( sda, False, myObj )

			self.parent.save()


		def allocate( self, destination, amount ):
			if self.parent.getObj().document_type != SourceDocumentType.PAYMENT and self.parent.getObj().document_type != SourceDocumentType.CREDIT_NOTE:
				raise BusLogError( 'You can not allocate this type of SourceDocument. You can only receive allocations.' )

			return destination.getAllocations().receive(
					self.parent,
					amount
				)


		def receive( self, source, amount ):

			if self.parent.getObj().document_type != SourceDocumentType.INVOICE and self.parent.getObj().document_type != SourceDocumentType.REFUND:
				raise BusLogError( 'You can not allocate this type of SourceDocument. You can only receive allocations.' )

			diff = self.parent.getTotals().getUnallocated()
			if amount > diff:
				raise BusLogError( 'The amount you want to allocate exceeds the amount that is outstanding.' )

			diff = source.getTotals().getUnallocated()
			if amount > diff:
				raise BusLogError( 'The amount you want to allocate exceeds the amount that is available for allocation.' )

			sda = SourceDocumentAllocation()
			sda.source = source.getObj()
			sda.destination = self.parent.getObj()
			sda.amount = amount
			sda.save()

			source.getObj().allocated += amount
			source.save()

			self.parent.getObj().allocated += amount
			self.parent.save()


	def getAllocations( self ):
		return self.Allocations( self )




