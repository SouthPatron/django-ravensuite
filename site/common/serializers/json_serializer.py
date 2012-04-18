

from django.utils.encoding import smart_unicode, is_protected_type

from base import Base

import json

class Serializer( Base ):

	def _dumps( self, key, value ):
		self.stream.write( u"{} : {}".format( json.dumps( key, ensure_ascii = False ), json.dumps( value, ensure_ascii = False )) )

	def straight_serialize( self, obj ):
		json.dump( obj, fp = self.stream, ensure_ascii = False )

	def start_serialization( self ):
		self.stream.write( "[" )

	def end_serialization( self ):
		self.stream.write( "]" )

	def start_object( self, obj ):
		self.stream.write( "{" )

	def end_object( self, obj ):
		self.stream.write( "}" )

	def object_separator( self, obj ):
		self.stream.write( ", " )

	def field_separator( self, obj ):
		self.stream.write( ", " )

	def handle_kvp( self, key, value ):
		self._dumps( key, value )

	def handle_field( self, obj, field, name = None):
		value = field._get_val_from_obj(obj)
		newval = value

		if is_protected_type(value):
			newval = value
		else:
			newval = field.value_to_string(obj)

		self._dumps( name or field.name, newval )


	def handle_fk_field(self, obj, field):
		if self.use_natural_keys and hasattr(field.rel.to, 'natural_key'):
			related = getattr(obj, field.name)
			if related:
				value = related.natural_key()
			else:
				value = None
		else:
			value = getattr(obj, field.get_attname())
		self._dumps( field.name, value )

	def handle_m2m_field(self, obj, field):
		if field.rel.through._meta.auto_created:
			if self.use_natural_keys and hasattr(field.rel.to, 'natural_key'):
				m2m_value = lambda value: value.natural_key()
			else:
				m2m_value = lambda value: smart_unicode(value._get_pk_val(), strings_only=True)

			self._dumps( field.name, [m2m_value(related)
						for related in getattr(obj, field.name).iterator()]
					)


