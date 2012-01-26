from django import template

from common.busobj.org import InvoiceObj, PaymentObj, CreditNoteObj
from common.models import SourceDocumentType

register = template.Library()


class GetDocumentObj( template.Node ):
	def __init__( self, sdo_name, var_name ):
		self.sdo = template.Variable( sdo_name )
		self.var_name = var_name
	
	def render( self, context ):
		obj = None

		try:
			sdo = self.sdo.resolve( context )

			if sdo.document_type == SourceDocumentType.INVOICE:
				obj = InvoiceObj()

			if sdo.document_type == SourceDocumentType.PAYMENT:
				obj = PaymentObj()

			if sdo.document_type == SourceDocumentType.CREDIT_NOTE:
				obj = CreditNoteObj()

			obj.wrap( sdo )

		except:
			pass

		context[ self.var_name ] = obj
		return ''


import re

@register.tag( name='get_document_obj' )
def get_document_obj( parser, token ):
	""" Encapsulates the SourceDocument model provided into a Business Object.

	"""

	try:
		tag_name, arg = token.contents.split( None, 1 )
	except ValueError:
		raise template.TemplateSyntaxError( '{} tag requires arguments'.format( token.contents.split()[0] ) )

	m = re.search( r'(.*?) as (\w+)', arg )
	if not m:
		raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name )

	sdo_name, var_name = m.groups()
	return GetDocumentObj( sdo_name, var_name )

