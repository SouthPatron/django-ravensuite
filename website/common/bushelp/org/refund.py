

from common.models import *
from common.bushelp.org.allocator import *
from common.bushelp.org.actions import *

from common.busobj.org import RefundObj


class RefundHelper( object ):
	def __init__( self ):
		super( RefundHelper, self ).__init__()


	@staticmethod
	def create( source, amount, refund_date ):

		obj = RefundObj()
		obj.initialize( source, amount, refund_date )

		obj.getLines().add(
			'Refund from {}'.format( source.getObj().refnum ),
			100,
			amount,
			TaxRate.NONE
		)


		ac = ActionFactory.instantiate( obj )
		ac.apply()

		al = Allocator()
		al.allocate( source, obj, amount )

		return obj


	@staticmethod
	def void( ref ):
		al = Allocator()
		al.clear( ref )

		ActionFactory.instantiate( ref ).void()

