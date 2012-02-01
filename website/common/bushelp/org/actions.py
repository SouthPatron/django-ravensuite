
from common.models import *
from common.exceptions import *

from common.buslog.org import AccountBusLog



class InvoiceActions( object ):
	def __init__( self, sdo ):
		super( InvoiceActions, self ).__init__()
		self.sdo = sdo


	def delete( self ):
		if self.sdo.getObj().document_state == SourceDocumentState.FINAL:
			raise BusLogError( 'This invoice has already been finalized. Try voiding it instead.' )
		if self.sdo.getObj().document_state == SourceDocumentState.VOID:
			raise BusLogError( 'This invoice has already been voided. It can not be removed.' )

		self.sdo.getObj().delete()


	def finalize( self ):
		ns = self.sdo.getObj().document_state

		if ns != SourceDocumentState.DRAFT:
			raise BusLogError( 'This invoice can not be finalized because it is not a draft.' )

		self.sdo.getObj().document_state = SourceDocumentState.FINAL
		self.sdo.save()

		AccountBusLog.adjust(
			self.sdo.getObj().client.account,
			self.sdo.getSpecs().getInvoiceDate(),
			'INVOICE',
			'Invoice {}'.format( self.sdo.getObj().refnum ),
			long(0) - (self.sdo.getTotals().getTotal()),
			self.sdo.getObj(),
			''
		)

	def void( self ):

		if self.sdo.getAllocations().all().count() > 0:
			raise BusLogError( 'There are still allocations associated with this source document. Please clear them first.' )


		ns = self.sdo.getObj().document_state

		if ns != SourceDocumentState.FINAL:
			raise BusLogError( 'This invoice can not be voided because it is not yet finalized.' )

		self.sdo.getObj().document_state = SourceDocumentState.VOID
		self.sdo.save()

		AccountBusLog.adjust(
			self.sdo.getObj().client.account,
			self.sdo.getSpecs().getInvoiceDate(),
			'VOID',
			'Void of Invoice {}'.format( self.sdo.getObj().refnum ),
			(self.sdo.getTotals().getTotal()),
			self.sdo.getObj(),
			''
		)



class PaymentActions( object ):
	def __init__( self, sdo ):
		super( PaymentActions, self ).__init__()
		self.sdo = sdo

	def delete( self ):
		if self.sdo.getObj().document_state == SourceDocumentState.FINAL:
			raise BusLogError( 'This payment has already been finalized. Try voiding it instead.' )
		if self.sdo.getObj().document_state == SourceDocumentState.VOID:
			raise BusLogError( 'This payment has already been voided. It can not be removed.' )

		self.sdo.getObj().delete()

	def finalize( self ):
		ns = self.sdo.getObj().document_state

		if ns != SourceDocumentState.DRAFT:
			raise BusLogError( 'This payment can not be finalized because it is not a draft.' )

		if self.sdo.getTotals().getTotal() <= 0:
			raise BusLogError( 'The payment amount has to be greater than zero.' )

		self.sdo.getObj().document_state = SourceDocumentState.FINAL
		self.sdo.save()

		AccountBusLog.adjust(
			self.sdo.getObj().client.account,
			self.sdo.getSpecs().getPaymentDate(),
			'PAYMENT',
			'Payment {}'.format( self.sdo.getObj().refnum ),
			self.sdo.getTotals().getTotal(),
			self.sdo.getObj(),
			''
		)

	def void( self ):
		if self.sdo.getAllocations().all().count() > 0:
			raise BusLogError( 'There are still allocations associated with this source document. Please clear them first.' )


		ns = self.sdo.getObj().document_state

		if ns != SourceDocumentState.FINAL:
			raise BusLogError( 'This payment can not be voided because it is not yet finalized.' )

		self.sdo.getObj().document_state = SourceDocumentState.VOID
		self.sdo.save()

		AccountBusLog.adjust(
			self.sdo.getObj().client.account,
			self.sdo.getSpecs().getPaymentDate(),
			'VOID',
			'Void of Payment {}'.format( self.sdo.getObj().refnum ),
			long(0) - (self.sdo.getTotals().getTotal()),
			self.sdo.getObj(),
			''
		)


class RefundActions( object ):
	def __init__( self, sdo ):
		super( RefundActions, self ).__init__()
		self.sdo = sdo

	def delete( self ):
		if self.sdo.getObj().document_state == SourceDocumentState.FINAL:
			raise BusLogError( 'This refund has already been finalized. Try voiding it instead.' )
		if self.sdo.getObj().document_state == SourceDocumentState.VOID:
			raise BusLogError( 'This refund has already been voided. It can not be removed.' )

		self.sdo.getObj().delete()

	def finalize( self ):
		ns = self.sdo.getObj().document_state

		if ns != SourceDocumentState.DRAFT:
			raise BusLogError( 'This refund can not be finalized because it is not a draft.' )

		if self.sdo.getTotals().getTotal() <= 0:
			raise BusLogError( 'The refund amount has to be greater than zero.' )

		self.sdo.getObj().document_state = SourceDocumentState.FINAL
		self.sdo.save()

		AccountBusLog.adjust(
			self.sdo.getObj().client.account,
			self.sdo.getSpecs().getRefundDate(),
			'REFUND',
			'Refund {}'.format( self.sdo.getObj().refnum ),
			(long(0) - self.sdo.getTotals().getTotal()),
			self.sdo.getObj(),
			''
		)

	def void( self ):
		if self.sdo.getAllocations().all().count() > 0:
			raise BusLogError( 'There are still allocations associated with this source document. Please clear them first.' )


		ns = self.sdo.getObj().document_state

		if ns != SourceDocumentState.FINAL:
			raise BusLogError( 'This refund can not be voided because it is not yet finalized.' )

		self.sdo.getObj().document_state = SourceDocumentState.VOID
		self.sdo.save()

		AccountBusLog.adjust(
			self.sdo.getObj().client.account,
			self.sdo.getSpecs().getRefundDate(),
			'VOID',
			'Void of Refund {}'.format( self.sdo.getObj().refnum ),
			self.sdo.getTotals().getTotal(),
			self.sdo.getObj(),
			''
		)





class CreditNoteActions( object ):
	def __init__( self, sdo ):
		super( CreditNoteActions, self ).__init__()
		self.sdo = sdo

	def delete( self ):
		if self.sdo.getObj().document_state == SourceDocumentState.FINAL:
			raise BusLogError( 'This credit note has already been finalized. Try voiding it instead.' )
		if self.sdo.getObj().document_state == SourceDocumentState.VOID:
			raise BusLogError( 'This credit note has already been voided. It can not be removed.' )

		self.sdo.getObj().delete()

	def finalize( self ):
		ns = self.sdo.getObj().document_state

		if ns != SourceDocumentState.DRAFT:
			raise BusLogError( 'This credit note can not be finalized because it is not a draft.' )

		self.sdo.getObj().document_state = SourceDocumentState.FINAL
		self.sdo.save()

		AccountBusLog.adjust(
			self.sdo.getObj().client.account,
			self.sdo.getSpecs().getCreditNoteDate(),
			'CREDIT NOTE',
			'CreditNote {}'.format( self.sdo.getObj().refnum ),
			(self.sdo.getTotals().getTotal()),
			self.sdo.getObj(),
			''
		)

	def void( self ):
		if self.sdo.getAllocations().all().count() > 0:
			raise BusLogError( 'There are still allocations associated with this source document. Please clear them first.' )


		ns = self.sdo.getObj().document_state

		if ns != SourceDocumentState.FINAL:
			raise BusLogError( 'This credit note can not be voided because it is not yet finalized.' )

		self.sdo.getObj().document_state = SourceDocumentState.VOID
		self.sdo.save()

		AccountBusLog.adjust(
			self.sdo.getObj().client.account,
			self.sdo.getSpecs().getCreditNoteDate(),
			'VOID',
			'Void of CreditNote {}'.format( self.sdo.getObj().refnum ),
			(long(0) - (self.sdo.getTotals().getTotal())),
			self.sdo.getObj(),
			''
		)





class ActionFactory( object ):

	@staticmethod
	def instantiate( sdo ):
		
		obj = None

		if sdo.getObj().document_type == SourceDocumentType.INVOICE:
			obj = InvoiceActions( sdo )

		if sdo.getObj().document_type == SourceDocumentType.PAYMENT:
			obj = PaymentActions( sdo )

		if sdo.getObj().document_type == SourceDocumentType.CREDIT_NOTE:
			obj = CreditNoteActions( sdo )

		if sdo.getObj().document_type == SourceDocumentType.REFUND:
			obj = RefundActions( sdo )

		if obj is None:
			raise RuntimeError( 'Unknown document type' )

		return obj


