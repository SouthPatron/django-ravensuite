from __future__ import unicode_literals

from django.http import HttpResponseForbidden

from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render_to_response
from django.template import TemplateDoesNotExist, RequestContext
from django.http import HttpResponse, Http404, HttpResponseForbidden

from common.serializers.serializer import Serializer


class RestForbidden( Exception ):
	pass


class RestfulView( View ):

	# ************** Class Members

	template_name = None
	url_kwargs = None

	supported_formats = {
		'json' : 'application/json'
	}

	# ************** Override these within your inherited classes

	def create_object( self, request, data, *args, **kwargs ):
		raise RestForbidden()

	def delete_object( self, request, *args, **kwargs ):
		raise RestForbidden()

	def get_extra( self, request, *args, **kwargs ):
		return None

	def get_object( self, request, *args, **kwargs ):
		return None

	def get_object_list( self, request, *args, **kwargs ):
		return None
	
	def update_object( self, request, data, *args, **kwargs ):
		raise RestForbidden()


	# ************** Initialization and Support Methods
	
	def _preload( self, request, *args, **kwargs ):
		self.dataset[ 'kwargs' ] = self.url_kwargs
		self.dataset[ 'instance' ] = self.get_object( request, *args, **kwargs )
		self.dataset[ 'object_list' ] = self.get_object_list( request, *args, **kwargs )
		self.dataset[ 'extra' ] = self.get_extra( request, *args, **kwargs )


	def get_template_name( self, method, fmt = None ):
		if self.template_name is None:
			raise RuntimeError( 'template_name has not been defined in instance' )
		ntn = '{}.{}.{}'.format( self.template_name, method, fmt or self.api_format )
		return ntn

	# ************** Overridden View methods

	@csrf_exempt
	def dispatch( self, request,  *args, **kwargs ):

		# Initialize empty dataset
		self.dataset = {
				'instance' : None,
				'object_list' : None,
				'extra' : None,
				'kwargs' : None,
			}

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
			ans = super( RestfulView, self ).dispatch( request, *args, **kwargs )
			return ans
		except RestForbidden:
			return HttpResponseForbidden()




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
		self._preload( request, *args, **kwargs )
		newo = self.delete_object( request, *args, **kwargs )
		self.dataset[ 'result' ] = newo

		try:
			ntn = self.get_template_name( 'delete' )
			response = render_to_response(
						ntn,
						self.dataset,
						context_instance=RequestContext(request)
					)
		except TemplateDoesNotExist:
			response = HttpResponse( status = 204 )

		response[ 'Content-Type' ] = self.supported_formats[ self.api_format ]
		response[ 'Cache-Control' ] = 'no-cache'
		return response


	def get( self, request, *args, **kwargs ):
		self._preload( request, *args, **kwargs )

		try:
			ntn = self.get_template_name( 'get' )
			response = render_to_response(
						ntn,
						self.dataset,
						context_instance=RequestContext(request)
					)
		except TemplateDoesNotExist:
			response = HttpResponse( status = 200 )
			response[ 'Content-Type' ] = self.supported_formats[ self.api_format ]
			response[ 'Cache-Control' ] = 'no-cache'

			target = self.dataset[ 'object_list' ] or [ self.dataset[ 'instance' ] ]

			Serializer.serialize(
					self.api_format,
					target,
					stream = response,
					reference_key = 'refnum'
				)
			return response


		response[ 'Content-Type' ] = self.supported_formats[ self.api_format ]
		response[ 'Cache-Control' ] = 'no-cache'
		return response

	def post( self, request, *args, **kwargs ):
		""" Handles HTTP POST (create) requests.

		create_object hook should return the object created, if any.

		If an object is created, then:
			Object should support get_absolute_method
			201 is returned with the Location header set.
			Template should exist.

		If an object is not created, then:
			200 is returned if there is content in the template
			204 is returned if there is no template
		"""

		self._preload( request, *args, **kwargs )
		data = self._get_body_data( request, self.api_format )

		newo = self.create_object( request, data, *args, **kwargs )
		self.dataset[ 'result' ] = newo

		try:
			ntn = self.get_template_name( 'post' )
			response = render_to_response(
						ntn,
						self.dataset,
						context_instance=RequestContext(request)
					)

		except TemplateDoesNotExist:
			response = HttpResponse( status = 204 )

		response[ 'Content-Type' ] = self.supported_formats[ self.api_format ]
		response[ 'Cache-Control' ] = 'no-cache'

		if newo is not None:
			response[ 'Location' ] = newo.get_absolute_url()
			response.status_code = 201

		return response


	def put( self, request, *args, **kwargs ):
		self._preload( request, *args, **kwargs )
		data = self._get_body_data( request, self.api_format )

		newo = self.update_object( request, data, *args, **kwargs )
		self.dataset[ 'result' ] = newo

		try:
			ntn = self.get_template_name( 'put' )
			response = render_to_response(
						ntn,
						self.dataset,
						context_instance=RequestContext(request)
					)
		except TemplateDoesNotExist:
			response = HttpResponse( status = 204 )

		response[ 'Content-Type' ] = self.supported_formats[ self.api_format ]
		response[ 'Cache-Control' ] = 'no-cache'
		return response


#	Responses:
#		Success	- 200 (content)
#		SuccessNoContent - 204
#		Created - 201 (content) (location header)
#		Accepted - 202




