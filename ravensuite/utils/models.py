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




# --- MoneyField ------------------------------------------------

class MoneyField( models.DecimalField ):
	""" Convenience class which is a DecimalField with 19 digits and 2
		decimal places.
	"""
	def __init__( self, *args, **kwargs ):
		if 'max_digits' not in kwargs:
			kwargs[ 'max_digits' ] = 19

		if 'decimal_places' not in kwargs:
			kwargs[ 'decimal_places' ] = 2

		return super( MoneyField, self ).__init__( *args, **kwargs )

try:
	from south.modelsinspector import add_introspection_rules
	add_introspection_rules([], ["^sp\.models\.MoneyField"])
except ImportError, ie:
	""" Presumably, south is not installed. So ... """
	pass



