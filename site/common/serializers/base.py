
from StringIO import StringIO

from django.utils.encoding import smart_unicode


class Base( object ):
	def __init__( self, *args, **kwargs ):
		super( Base, self ).__init__( *args, **kwargs )
		self.stream = None

	def getvalue( self ):
		if callable(getattr(self.stream, 'getvalue', None)):
			return self.stream.getvalue()


	def serialize( self, queryset, **kwargs ):
		self.stream = kwargs.pop( 'stream', StringIO() )
		self.selected_fields = kwargs.pop( 'fields', None)
		self.use_natural_keys = kwargs.pop( 'use_natural_keys', False)
		self.reference_key = kwargs.pop( 'reference_key', 'id' )


		self.start_serialization()

		for i, obj in enumerate( queryset ):

			if i != 0:
				self.object_separator( obj )

			self.start_object(obj)

			concrete_model = obj._meta.concrete_model

			firstField = True

			for field in concrete_model._meta.local_fields:
				if field.serialize:
					if field.rel is None:
						if self.selected_fields is None or field.attname in self.selected_fields:
							if firstField is False:
								self.field_separator( obj )
							else:
								firstField = False
							self.handle_field(obj, field )
					else:
						if self.selected_fields is None or field.attname[:-3] in self.selected_fields:
							if firstField is False:
								self.field_separator( obj )
							else:
								firstField = False
							self.handle_fk_field(obj, field )

			for field in concrete_model._meta.many_to_many:
				if field.serialize:
					if self.selected_fields is None or field.attname in self.selected_fields:
						if firstField is False:
							self.field_separator( obj )
						else:
							firstField = False
						self.handle_m2m_field( obj, field )


			if firstField is False:
				self.field_separator( obj )

			field = getattr( obj, self.reference_key, None )
			if field is not None:
				self.handle_kvp( "pk", field )

			self.end_object(obj)

		self.end_serialization()
		return self.getvalue()




