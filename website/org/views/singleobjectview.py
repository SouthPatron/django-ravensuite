from __future__ import unicode_literals

from django.http import HttpResponseServerError, HttpResponseForbidden


from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404

from ..models import *
from base import Base

class SingleObjectView( Base ):

	# ************** Probably want to override

	def get_extra( self, request, obj, fmt, *args, **kwargs ):
		return None

	def get_object( self, request, *args, **kwargs ):
		return None
	
	def delete_object( self, request, ob, *args, **kwargs ):
		return HttpResponseForbidden()

#	def update_object_<format>( self, request, obj, data, *args, **kwargs )
	

	# ************** HTTP Operations

	def get( self, request, *args, **kwargs ):
		fmt = self._parse_format( request )
		if fmt is None: return HttpResponseForbidden()

		ob = self.get_object( request, *args, **kwargs )
		if ob is None:
			self.not_found()

		extra = self.get_extra( request, ob, fmt, *args, **kwargs )
		ntn = self.get_template_name( 'get', fmt )

		response = render_to_response(
					ntn,
					{
						'instance' : ob,
						'extra' : extra,
						'kwargs' : self.url_kwargs,
					},
					context_instance=RequestContext(request)
				)

		response[ 'Content-Type' ] = self.supported_formats[ fmt ]
		return response

	
	def put( self, request, *args, **kwargs ):
		fmt = self._parse_format( request )
		if fmt is None: return HttpResponseForbidden()

		ob = self.get_object( request, *args, **kwargs )
		if ob is None:
			self.not_found()

		data = self._get_body_data( request, fmt )

		handler = getattr( self, 'update_object_{}'.format( fmt ), None )
		if handler is None:
			return HttpResponseForbidden()

		return handler( request, ob, data, *args, **kwargs )

	def post( self, request, *args, **kwargs ):
		"""
		Only accepts POST for HTML formats so that web forms work. Otherwise
		PUT is the correct method to use for updating in RESTful apps.
		"""
		fmt = self._parse_format( request )
		if fmt is None or fmt != 'html':
			return HttpResponseForbidden()

		return self.put( request, *args, **kwargs )


	def delete( self, request, *args, **kwargs ):
		fmt = self._parse_format( request )
		if fmt is None: return HttpResponseForbidden()

		ob = self.get_object( request, *args, **kwargs )
		if ob is None:
			self.not_found()

		extra = self.get_extra( request, ob, fmt, *args, **kwargs )
		ntn = self.get_template_name( 'delete', fmt )

		return self.delete_object( request, ob, *args, **kwargs )

