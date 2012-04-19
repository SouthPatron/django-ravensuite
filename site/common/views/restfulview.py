from __future__ import unicode_literals

from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404, HttpResponseForbidden

from common.serializers.serializer import Serializer

import collections
import json

class RestForbidden( Exception ):
	pass

class RestResponse( Exception ):
	def __init__( self, response, *args, **kwargs ):
		self.response = response
		super( RestResponse, self ).__init__( *args, **kwargs )

class RestfulView( View ):

	# ************** Class Members

	url_kwargs = None

	supported_formats = {
		'json' : 'application/json'
	}

	# ************** Override these within your inherited classes

	def create_object( self, request, data, *args, **kwargs ):
		raise RestForbidden()

	def delete_object( self, request, *args, **kwargs ):
		raise RestForbidden()

	def get_object( self, request, *args, **kwargs ):
		return self.not_found()

	def update_object( self, request, data, *args, **kwargs ):
		raise RestForbidden()

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


	# ************** Data Support Methods

	def _get_body_data( self, request, fmt ):
		if fmt == 'json':
			data = request.read()
			if data is None or len(data) == 0:
				return {}
			return json.loads( data )

		return None


	# ************** Response methods

	def not_found( self ):
		raise Http404( 'Object Not Found' )


	# ************** HTTP Operations

	def delete( self, request, *args, **kwargs ):
		obj = self.delete_object( request, *args, **kwargs )
		if isinstance( obj, collections.Iterable ) is False:
			obj = [ obj ]

		response = HttpResponse( status = 204 )
		response[ 'Content-Type' ] = self.supported_formats[ self.api_format ]
		response[ 'Cache-Control' ] = 'no-cache'

		if obj is not None:
			response.status_code = 200
			Serializer.serialize(
					self.api_format,
					obj,
					stream = response,
					reference_key = 'refnum'
				)
		return response


	def get( self, request, *args, **kwargs ):
		obj = self.get_object( request, *args, **kwargs )
		if obj is None:
			self.not_found()

		if isinstance( obj, collections.Iterable ) is False:
			obj = [ obj ]

		response = HttpResponse( status = 200 )
		response[ 'Content-Type' ] = self.supported_formats[ self.api_format ]
		response[ 'Cache-Control' ] = 'no-cache'

		Serializer.serialize(
				self.api_format,
				obj,
				stream = response,
				reference_key = 'refnum'
			)
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
		if isinstance( obj, collections.Iterable ) is False:
			obj = [ obj ]

		response = HttpResponse( status = 204 )
		response[ 'Content-Type' ] = self.supported_formats[ self.api_format ]
		response[ 'Cache-Control' ] = 'no-cache'

		if obj is not None:
			response[ 'Location' ] = obj.get_absolute_url()
			response.status_code = 201

			Serializer.serialize(
				self.api_format,
				obj,
				stream = response,
				reference_key = 'refnum'
			)

		return response


	def put( self, request, *args, **kwargs ):
		data = self._get_body_data( request, self.api_format )
		obj = self.update_object( request, data, *args, **kwargs )
		if isinstance( obj, collections.Iterable ) is False:
			obj = [ obj ]

		response = HttpResponse( status = 204 )
		response[ 'Content-Type' ] = self.supported_formats[ self.api_format ]
		response[ 'Cache-Control' ] = 'no-cache'

		if obj is not None:
			response.status_code = 200

			Serializer.serialize(
				self.api_format,
				obj,
				stream = response,
				reference_key = 'refnum'
			)

		return response


#	Responses:
#		Success	- 200 (content)
#		SuccessNoContent - 204
#		Created - 201 (content) (location header)
#		Accepted - 202




