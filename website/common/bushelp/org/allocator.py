

from django.db.models import Q

from common.models import SourceDocumentAllocation, SourceDocumentState, SourceDocumentType
from common.busobj.org import *
from common.busobj.org.factory import Factory


class Allocator( object ):

	def __init__( self ):
		super( Allocator, self ).__init__()

	def deallocate_one( self, reference, sda ):
		if sda.source == reference.getObj():
			distance = Factory.instantiate( sda.destination )
		else:
			distance = Factory.instantiate( sda.source )

		distance.getObj().allocated -= sda.amount
		distance.save()

		reference.getObj().allocated -= sda.amount
		reference.save()

		sda.delete()


	def deallocate( self, reference, sdaid ):

		try:
			sda = SourceDocumentAllocation.objects.get(
					Q( source = reference.getObj() ) | Q( destination = reference.getObj() ),
					id = sdaid
				)

			self.deallocate_one( reference, sda )
		except SourceDocumentAllocation.DoesNotExist:
			raise BusLogError( 'There was no such allocation with that id and reference.' )



	def clear( self, reference ):
		for sda in SourceDocumentAllocation.objects.filter( Q( source = reference.getObj() ) | Q( destination = reference.getObj() ) ):
			self.deallocate_one( reference, sda )


	def allocate( self, source, destination, amount ):

		# Is the destination a receivable?
		if destination.getObj().document_type != SourceDocumentType.INVOICE and destination.getObj().document_type != SourceDocumentType.REFUND:
			raise BusLogError( 'The allocation failed because the destination is not able to receive allocations.' )

		# Is the source a payable?
		if source.getObj().document_type != SourceDocumentType.CREDIT_NOTE and source.getObj().document_type != SourceDocumentType.PAYMENT:
			raise BusLogError( 'The allocation failed because the source is not able to be allocated.' )
	
		# Can destination receive amount?
		diff = destination.getTotals().getUnallocated()
		if amount > diff:
			raise BusLogError( 'The amount you want to allocate exceeds the amount that is outstanding.' )

		# Can source receive amount?
		diff = source.getTotals().getUnallocated()
		if amount > diff:
			raise BusLogError( 'The amount you want to allocate exceeds the amount that is available for allocation.' )

		# Allocate
		sda = SourceDocumentAllocation()
		sda.source = source.getObj()
		sda.destination = destination.getObj()
		sda.amount = amount
		sda.save()

		source.getObj().allocated += amount
		source.save()

		destination.getObj().allocated += amount
		destination.save()



