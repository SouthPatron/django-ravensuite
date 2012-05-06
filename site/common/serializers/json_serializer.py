
import datetime
import decimal

from django.utils.encoding import smart_unicode, is_protected_type

from base import Base

import json

class Serializer( Base ):

	def _dumps( self, key, value ):

		newkey = self.name_map.get( key, key )

		self.stream.write( u"{} : {}".format( json.dumps( newkey, ensure_ascii = False ), json.dumps( value, ensure_ascii = False )) )

	def start_collection( self ):
		self.stream.write( "[" )

	def end_collection( self ):
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

	def _handle(self, o):
		# See "Date Time String Format" in the ECMA-262 specification.
		if isinstance(o, datetime.datetime):
			r = o.isoformat()
			if o.microsecond:
				r = r[:23] + r[26:]
			if r.endswith('+00:00'):
				r = r[:-6] + 'Z'
			return r
		elif isinstance(o, datetime.date):
			return o.isoformat()
		elif isinstance(o, datetime.time):
			if is_aware(o):
				raise ValueError("JSON can't represent timezone-aware times.")
			r = o.isoformat()
			if o.microsecond:
				r = r[:12]
			return r
		elif isinstance(o, decimal.Decimal):
			return str(o)

		return o


	def handle_field( self, obj, field, name = None):
		value = field._get_val_from_obj(obj)
		newval = value

		if is_protected_type(value):
			newval = value
		else:
			newval = field.value_to_string(obj)

		newvy = self._handle( newval )

		self._dumps( name or field.name, newvy )


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


