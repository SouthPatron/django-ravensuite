from __future__ import unicode_literals

from django.db import models
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404, HttpResponseForbidden

from common.utils.class_loader import ClassLoader
from common.serializers.serializer import Serializer

import collections
import json
import re

class RestForbidden( Exception ):
	pass

class RestResponse( Exception ):
	def __init__( self, response, *args, **kwargs ):
		self.response = response
		super( RestResponse, self ).__init__( *args, **kwargs )


class RestfulLogic( object ):

#	class Meta:
#		allow_update = True
#		readonly = ( 'refnum', )
#		fields = ( 'refnum', 'trading_name', 'telephone_number', )
#		exclude = ( 'fax_number', )
#		include = ( 'id', )
#		name_map = { 'old_name' : 'new_name' }


	def __init__( self, view, *args, **kwargs ):
		super( RestfulLogic, self ).__init__( *args, **kwargs )
		self.view = view
		self.url_kwargs = view.url_kwargs

	def create_object( self, request, data, *args, **kwargs ):
		raise RestForbidden()

	def delete_object( self, request, *args, **kwargs ):
		raise RestForbidden()

	def get_object( self, request, *args, **kwargs ):
		return self.view.not_found()

#	def update_object( self, request, data, *args, **kwargs ):



class RestfulView( View ):

	# ************** Class Members

	base_module = ''
	restful_list = []
	logic = None

	url_kwargs = None

	supported_formats = {
		'json' : 'application/json'
	}

	# ************** Override these within your inherited classes

	def create_object( self, request, data, *args, **kwargs ):
		self._prepare( request, *args, **kwargs )
		return self.logic.create_object( request, data, *args, **kwargs )

	def delete_object( self, request, *args, **kwargs ):
		self._prepare( request, *args, **kwargs )
		return self.logic.delete_object( request, *args, **kwargs )

	def get_object( self, request, *args, **kwargs ):
		self._prepare( request, *args, **kwargs )
		return self.logic.get_object( request, *args, **kwargs )

	def update_object( self, request, data, *args, **kwargs ):
		self._prepare( request, *args, **kwargs )

		meta = getattr( self.logic, 'Meta', None )

		if meta is None or getattr( meta, 'allow_update', False ) is False:
			raise RestForbidden()

		if hasattr( self.logic, 'update_object' ) is True:
			return self.logic.update_object( request, data, *args, **kwargs )

		obj = self.get_object( request, *args, **kwargs )

		if isinstance( obj, models.Model ) is False:
			raise NotImplementedError( 'You must implement an update_object method in your logic class for non-model objects.' )

		return self.def_model_update( request, data, obj, meta, *args, **kwargs )


	# ************** Default Hooks

	def _def_model_update( self, obj, data, meta, field ):
		if not field.serialize:
			return False

		if field.primary_key is True:
			return False

		if field.rel is None:
			name = field.attname
		else:
			name = field.attname[:-3]

		# Get the name after mapping. confusing names, haha
		map_name = name
		if meta is not None:
			name_map = getattr( meta, 'name_map', {} )
			map_name = name_map.get( map_name, map_name )

		if map_name not in data:
			return False

		if meta is not None:
			if hasattr( meta, 'readonly' ) and name in meta.readonly:
				return False
			if hasattr( meta, 'exclude' ) and name in meta.exclude:
				return False
			if hasattr( meta, 'fields' ) and name not in meta.fields:
				return False

		setattr( obj, name, data[ map_name ] )
		return True


	def def_model_update( self, request, data, obj, meta, *args, **kwargs ):
		isDirty = False

		for field in obj._meta.local_fields:
			if self._def_model_update( obj, data, meta, field ) is True:
				isDirty = True

		for name in getattr( meta, 'include', [] ):
			field = obj._meta.get_field( name )
			if self._def_model_update( obj, data, meta, field ) is True:
				isDirty = True


		if isDirty is True:
			obj.save()
		
		return obj


	# ************** Overridden View methods

	@csrf_exempt
	def dispatch( self, request,  *args, **kwargs ):

		# Load the API format from URL format
		self.api_format = kwargs.get( 'api_format', 'json' )
		if self.api_format not in self.supported_formats:
			return self.not_found()

		# Load all the kwargs into a local attribute
		class IdObject( object ):
			pass
		self.url_kwargs = IdObject()
		for nm, val in kwargs.iteritems():
			setattr( self.url_kwargs, nm, val )

		try:
			return super( RestfulView, self ).dispatch( request, *args, **kwargs )
		except RestForbidden:
			return HttpResponseForbidden()
		except RestResponse, rr:
			return rr.response


	# ************** Support Methods

	def _get_body_data( self, request, fmt ):
		if fmt == 'json':
			data = request.read()
			if data is None or len(data) == 0:
				return {}
			return json.loads( data )

		return None

	def _search_match( self, request, *args, **kwargs ):
		node = kwargs[ 'node' ]
		for pair in self.restful_list:
			m = re.match( pair[0], node )
			if m is not None:
				return { 'args' : m.groupdict(), 'classname' : pair[1] }
		return None

	def _prepare( self, request, *args, **kwargs ):
		if self.logic is not None:
			return

		match = self._search_match( request, *args, **kwargs )
		if match is None:
			return self.not_found()

		# Append new args to self.url_kwargs
		for nm, val in match[ 'args' ].iteritems():
			setattr( self.url_kwargs, nm, val )

		# Instantiate the logic class
		logic = ClassLoader.load( '{}.{}'.format( self.base_module, match['classname'] ) )
		if logic is None:
			return self.not_found()
		self.logic = logic( self )


	# ************** Response methods

	def not_found( self ):
		raise Http404( 'Object Not Found' )


	# ************** Serialization with logic rules

	def flatten( self, response, obj ):

		if isinstance( obj, models.Model ) is True or isinstance( obj, models.query.QuerySet ) is True:
			meta = getattr( self.logic, 'Meta', {} )

			fields = getattr( meta, 'fields', None )
			exclude = getattr( meta, 'exclude', None )
			name_map = getattr( meta, 'name_map', {} )
			include = getattr( meta, 'include', None )

			Serializer.serialize(
					self.api_format,
					obj,
					stream = response,
					fields = fields,
					exclude = exclude,
					name_map = name_map,
					include = include
				)
		else:
			json.dump( obj, fp = response, ensure_ascii = False )




	# ************** HTTP Operations

	def delete( self, request, *args, **kwargs ):
		obj = self.delete_object( request, *args, **kwargs )

		response = HttpResponse( status = 204 )
		response[ 'Content-Type' ] = self.supported_formats[ self.api_format ]
		response[ 'Cache-Control' ] = 'no-cache'

		if obj is not None:
			response.status_code = 200
			self.flatten( response, obj )

		return response


	def get( self, request, *args, **kwargs ):
		obj = self.get_object( request, *args, **kwargs )
		if obj is None:
			self.not_found()

		response = HttpResponse( status = 200 )
		response[ 'Content-Type' ] = self.supported_formats[ self.api_format ]
		response[ 'Cache-Control' ] = 'no-cache'

		self.flatten( response, obj )
		return response

	def post( self, request, *args, **kwargs ):
		""" Handles HTTP POST (create) requests.

		create_object hook should return the object created, if any.

		If an object is created, then:
			Object should support get_absolute_method
			201 is returned with the Location header set.
			Template should exist.

		If an object is not created, then:
			204 is returned if there is no template
		"""
		data = self._get_body_data( request, self.api_format )
		obj = self.create_object( request, data, *args, **kwargs )

		response = HttpResponse( status = 204 )
		response[ 'Content-Type' ] = self.supported_formats[ self.api_format ]
		response[ 'Cache-Control' ] = 'no-cache'

		if obj is not None:
			response[ 'Location' ] = obj.get_absolute_url()
			response.status_code = 201

			self.flatten( response, obj )

		return response


	def put( self, request, *args, **kwargs ):
		data = self._get_body_data( request, self.api_format )
		obj = self.update_object( request, data, *args, **kwargs )

		response = HttpResponse( status = 204 )
		response[ 'Content-Type' ] = self.supported_formats[ self.api_format ]
		response[ 'Cache-Control' ] = 'no-cache'

		if obj is not None:
			response.status_code = 200

			self.flatten( response, obj )

		return response


#	Responses:
#		Success	- 200 (content)
#		SuccessNoContent - 204
#		Created - 201 (content) (location header)
#		Accepted - 202




