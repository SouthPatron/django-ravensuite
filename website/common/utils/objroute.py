
import re

from common.models import *


class ObjRoute( object ):

	@staticmethod
	def _get_invoice( blocks ):
		return Invoice.objects.get( client__organization__refnum = blocks[0], client__refnum = blocks[1], refnum = blocks[2] )


	@staticmethod
	def _get_payment( blocks ):
		return Payment.objects.get( client__organization__refnum = blocks[0], client__refnum = blocks[1], refnum = blocks[2] )

	@staticmethod
	def _get_refund( blocks ):
		return Refund.objects.get( client__organization__refnum = blocks[0], client__refnum = blocks[1], refnum = blocks[2] )


	@staticmethod
	def get( route ):
		blocks = re.split( u'\s+', route )

		try:
			if blocks[0] == 'org.client.invoice':
				return ObjRoute._get_invoice( blocks[1:] )

			if blocks[0] == 'org.client.payment':
				return ObjRoute._get_payment( blocks[1:] )

			if blocks[0] == 'org.client.refund':
				return ObjRoute._get_refund( blocks[1:] )

		except:
			return None

