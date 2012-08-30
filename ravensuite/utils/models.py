from django.db import models

class MemoryModel( models.Model ):
	""" This is your basic django.db.models.Model which keeps the
		the original field values in an attribute called 'original' -
		if the primary key is defined.
	"""
	class Meta:
		abstract = True

	def __init__( self, *args, **kwargs ):
		rc = super( MemoryModel, self ).__init__( *args, **kwargs )

		class oldval( object ):
			pass

		if self.pk is not None:
			self.original = oldval()
			for fld in self._meta.fields:
				setattr( self.original, fld.name, getattr( self, fld.name ) )
		return rc


