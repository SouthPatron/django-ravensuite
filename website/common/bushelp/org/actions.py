from django.utils.translation import ugettext as _

from common.models import *
from common.exceptions import *
from common.buslog.org import AccountBusLog


class InvoiceActions( object ):
	def __init__( self, sdo ):
		super( InvoiceActions, self ).__init__()
		self.sdo = sdo


	def delete( self ):
		if self.sdo.getObj().document_state == SourceDocumentState.FINAL:
			raise BLE_ProcessFlowError( _('BLE_40001') )
		if self.sdo.getObj().document_state == SourceDocumentState.VOID:
			raise BLE_ProcessFlowError( _('BLE_40002') )

		self.sdo.getObj().delete()


	def finalize( self ):
		ns = self.sdo.getObj().document_state

		if ns != SourceDocumentState.DRAFT:
			raise BLE_ProcessFlowError( _('BLE_40003') )

		self.sdo.getObj().document_state = SourceDocumentState.FINAL
		self.sdo.save()

		AccountBusLog.adjust(
			self.sdo.getObj().client.account,
			self.sdo.getSpecs().getInvoiceDate(),
			_('BNAV_40101'),
			'Invoice {}'.format( self.sdo.getObj().refnum ),
			long(0) - (self.sdo.getTotals().getTotal()),
			self.sdo.getObj(),
			''
		)

	def void( self ):

		if self.sdo.getAllocations().all().count() > 0:
			raise BLE_ProcessFlowError( _('BLE_40004') )


		ns = self.sdo.getObj().document_state

		if ns != SourceDocumentState.FINAL:
			raise BLE_ProcessFlowError( _('BLE_40005') )

		self.sdo.getObj().document_state = SourceDocumentState.VOID
		self.sdo.save()

		AccountBusLog.adjust(
			self.sdo.getObj().client.account,
			self.sdo.getSpecs().getInvoiceDate(),
			_('BNAV_40105'),
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
			raise BLE_ProcessFlowError( _('BLE_40101') )
		if self.sdo.getObj().document_state == SourceDocumentState.VOID:
			raise BLE_ProcessFlowError( _('BLE_40102') )

		self.sdo.getObj().delete()

	def finalize( self ):
		ns = self.sdo.getObj().document_state

		if ns != SourceDocumentState.DRAFT:
			raise BLE_ProcessFlowError( _('BLE_40103') )

		if self.sdo.getTotals().getTotal() <= 0:
			raise BLE_ValueRangeError( _('BLE_40104') )

		self.sdo.getObj().document_state = SourceDocumentState.FINAL
		self.sdo.save()

		AccountBusLog.adjust(
			self.sdo.getObj().client.account,
			self.sdo.getSpecs().getPaymentDate(),
			_('BNAV_40103'),
			'Payment {}'.format( self.sdo.getObj().refnum ),
			self.sdo.getTotals().getTotal(),
			self.sdo.getObj(),
			''
		)

	def void( self ):
		if self.sdo.getAllocations().all().count() > 0:
			raise BLE_ProcessFlowError( _('BLE_40105') )


		ns = self.sdo.getObj().document_state

		if ns != SourceDocumentState.FINAL:
			raise BLE_ProcessFlowError( _('BLE_40106') )

		self.sdo.getObj().document_state = SourceDocumentState.VOID
		self.sdo.save()

		AccountBusLog.adjust(
			self.sdo.getObj().client.account,
			self.sdo.getSpecs().getPaymentDate(),
			_('BNAV_40105'),
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
			raise BLE_ProcessFlowError( _('BLE_40201') )
		if self.sdo.getObj().document_state == SourceDocumentState.VOID:
			raise BLE_ProcessFlowError( _('BLE_40202') )

		self.sdo.getObj().delete()

	def finalize( self ):
		ns = self.sdo.getObj().document_state

		if ns != SourceDocumentState.DRAFT:
			raise BLE_ProcessFlowError( _('BLE_40203') )

		if self.sdo.getTotals().getTotal() <= 0:
			raise BLE_ValueRangeError( _('BLE_40204') )

		self.sdo.getObj().document_state = SourceDocumentState.FINAL
		self.sdo.save()

		AccountBusLog.adjust(
			self.sdo.getObj().client.account,
			self.sdo.getSpecs().getRefundDate(),
			_('BNAV_40104'),
			'Refund {}'.format( self.sdo.getObj().refnum ),
			(long(0) - self.sdo.getTotals().getTotal()),
			self.sdo.getObj(),
			''
		)

	def void( self ):
		if self.sdo.getAllocations().all().count() > 0:
			raise BLE_ProcessFlowError( _('BLE_40205') )


		ns = self.sdo.getObj().document_state

		if ns != SourceDocumentState.FINAL:
			raise BLE_ProcessFlowError( _('BLE_40206') )

		self.sdo.getObj().document_state = SourceDocumentState.VOID
		self.sdo.save()

		AccountBusLog.adjust(
			self.sdo.getObj().client.account,
			self.sdo.getSpecs().getRefundDate(),
			_('BNAV_40105'),
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
			raise BLE_ProcessFlowError( _('BLE_40301') )
		if self.sdo.getObj().document_state == SourceDocumentState.VOID:
			raise BLE_ProcessFlowError( _('BLE_40302') )

		self.sdo.getObj().delete()

	def finalize( self ):
		ns = self.sdo.getObj().document_state

		if ns != SourceDocumentState.DRAFT:
			raise BLE_ProcessFlowError( _('BLE_40303') )

		self.sdo.getObj().document_state = SourceDocumentState.FINAL
		self.sdo.save()

		AccountBusLog.adjust(
			self.sdo.getObj().client.account,
			self.sdo.getSpecs().getCreditNoteDate(),
			_('BNAV_40102'),
			'CreditNote {}'.format( self.sdo.getObj().refnum ),
			(self.sdo.getTotals().getTotal()),
			self.sdo.getObj(),
			''
		)

	def void( self ):
		if self.sdo.getAllocations().all().count() > 0:
			raise BLE_ProcessFlowError( _('BLE_40305') )


		ns = self.sdo.getObj().document_state

		if ns != SourceDocumentState.FINAL:
			raise BLE_ProcessFlowError( _('BLE_40306') )

		self.sdo.getObj().document_state = SourceDocumentState.VOID
		self.sdo.save()

		AccountBusLog.adjust(
			self.sdo.getObj().client.account,
			self.sdo.getSpecs().getCreditNoteDate(),
			_('BNAV_40105'),
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
			raise BLE_DevError( _('BLE_80002') )

		return obj


