
from StringIO import StringIO
from django.utils.encoding import smart_unicode
from django.db.models import Model

import collections

class Base( object ):
	def __init__( self, *args, **kwargs ):
		super( Base, self ).__init__( *args, **kwargs )
		self.stream = None

	def getvalue( self ):
		if callable(getattr(self.stream, 'getvalue', None)):
			return self.stream.getvalue()

	def _serialize_model( self, obj ):
		self.start_object(obj)

		concrete_model = obj._meta.concrete_model

		firstField = True

		for field in concrete_model._meta.local_fields:
			if field.serialize:
				if field.rel is None:
					if self.selected_fields is None or field.attname in self.selected_fields:
						if self.excluded_fields is None or field.attname not in self.excluded_fields:
							if firstField is False:
								self.field_separator( obj )
							else:
								firstField = False
							self.handle_field( obj, field )
				else:
					if self.selected_fields is None or field.attname[:-3] in self.selected_fields:
						if self.excluded_fields is None or field.attname not in self.excluded_fields:
							if firstField is False:
								self.field_separator( obj )
							else:
								firstField = False
							self.handle_fk_field(obj, field )

		for field in concrete_model._meta.many_to_many:
			if field.serialize:
				if self.selected_fields is None or field.attname in self.selected_fields:
					if self.excluded_fields is None or field.attname not in self.excluded_fields:
						if firstField is False:
							self.field_separator( obj )
						else:
							firstField = False
						self.handle_m2m_field( obj, field )


		if self.included_fields is not None:
			for key in self.included_fields:
				if firstField is False:
					self.field_separator( obj )
				else:
					firstField = False

				field = getattr( obj, key )
				self.handle_kvp( key, field )

		self.end_object(obj)


	def _serialize_object( self, obj ):

		if isinstance( obj, Model ) is True:
			self._serialize_model( obj )
		else:
			self.straight_serialize( obj )



	def serialize( self, dimobj, **kwargs ):
		self.stream = kwargs.pop( 'stream', StringIO() )
		self.selected_fields = kwargs.pop( 'fields', None)
		self.excluded_fields = kwargs.pop( 'exclude', None)
		self.included_fields = kwargs.pop( 'include', None)
		self.use_natural_keys = kwargs.pop( 'use_natural_keys', False)
		self.name_map = kwargs.pop( 'name_map', {} )


		if isinstance( dimobj, collections.Iterable ) is False:
			self._serialize_object( dimobj )
		else:
			self.start_collection()
			for i, obj in enumerate( dimobj ):
				if i != 0:
					self.object_separator( obj )

				self._serialize_object( obj )
			self.end_collection()

		return self.getvalue()


