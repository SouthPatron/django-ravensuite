from __future__ import unicode_literals

from django.http import HttpResponseServerError, HttpResponseForbidden


from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.base import View
from django.http import Http404

from base import Base

class ListView( Base ):


	# ************** Probably want to override

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return None

	def get_object_list( self, request, *args, **kwargs ):
		return None
	
#	def create_object_<format>( self, request, data, *args, **kwargs )
	

	# ************** HTTP Operations

	def get( self, request, *args, **kwargs ):
		fmt = self._parse_format( request )
		if fmt is None: return HttpResponseForbidden()

		obj_list = self.get_object_list( request, *args, **kwargs )
		if obj_list is None:
			self.not_found()

		extra = self.get_extra( request, obj_list, fmt, *args, **kwargs )
		ntn = self.get_template_name( 'get', fmt )

		response = render_to_response(
					ntn,
					{
						'object_list' : obj_list,
						'extra' : extra,
					},
					context_instance=RequestContext(request)
				)

		response[ 'Content-Type' ] = self.supported_formats[ fmt ]
		return response

	
	def put( self, request, *args, **kwargs ):
		fmt = self._parse_format( request )
		if fmt is None: return HttpResponseForbidden()
	
		try:
			data = self._get_body_data( request, fmt )
		except:
			return HttpResponseServerError()

		handler = getattr( self, 'create_object_{}'.format( fmt ), None )
		if handler is None:
			return HttpResponseForbidden()

		return handler( request, data, *args, **kwargs )


