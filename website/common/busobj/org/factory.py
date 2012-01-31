
from common.models import SourceDocumentType
from common.busobj.org import InvoiceObj, PaymentObj, CreditNoteObj, RefundObj


class Factory( object ):

	@staticmethod
	def instantiate( sdo ):
		obj = None

		if sdo.document_type == SourceDocumentType.INVOICE:
			obj = InvoiceObj()

		if sdo.document_type == SourceDocumentType.PAYMENT:
			obj = PaymentObj()

		if sdo.document_type == SourceDocumentType.CREDIT_NOTE:
			obj = CreditNoteObj()

		if sdo.document_type == SourceDocumentType.REFUND:
			obj = RefundObj()


		if obj is None:
			raise RuntimeError( 'Unknown SourceDocumentType' )

		obj.wrap( sdo )

		return obj


