from __future__ import unicode_literals

from django.http import HttpResponseServerError


from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.views.generic.base import View
from django.http import Http404


from ..models import *

class Base( View ):
	template_name = 'pages/org/org/index'

	supported_formats = {
		'html' : 'text/html',
		'json' : 'text/json',
	}

	# ************** Probably want to override

	def get_extra( self, request, obj, fmt, *args, **kwargs ):
		return None

	def get_object( self, request, *args, **kwargs ):
		return None
	
	def delete_object( self, request, ob, *args, **kwargs ):
		ob.delete()

	# ************** Unlikely to override

	def get_template_name( self, base, method, fmt ):
		ntn = '{}.{}.{}'.format( base, method, fmt )
		return ntn
	

	# ************** Probably won't override
	
	def not_found( self ):
		raise Http404( 'Object Not Found' )



	# ************** HTTP Operations

	def get( self, request, *args, **kwargs ):
		fmt = request.GET.get( 'format', 'html' )
		if fmt not in self.supported_formats:
			return HttpResponseServerError()

		ob = self.get_object( request, *args, **kwargs )
		if ob is None:
			self.not_found()

		extra = self.get_extra( request, ob, fmt, *args, **kwargs )
		ntn = self.get_template_name( self.template_name, 'get', fmt )

		response = render_to_response(
					ntn,
					{
						'instance' : ob,
						'extra' : extra,
					},
					context_instance=RequestContext(request)
				)

		response[ 'Content-Type' ] = self.supported_formats[ fmt ]
		return response

	
	def post( self, request, *args, **kwargs ):
		return redirect( 'org-index' )


	def put( self, request, *args, **kwargs ):
		return redirect( 'org-index' )


	def delete( self, request, *args, **kwargs ):
		fmt = request.GET.get( 'format', 'html' )
		if fmt not in self.supported_formats:
			return HttpResponseServerError()

		ob = self.get_object( request, *args, **kwargs )
		if ob is None:
			self.not_found()

		extra = self.get_extra( request, ob, fmt, *args, **kwargs )
		result = self.delete_object( ob )

		ntn = self.get_template_name( self.template_name, 'delete', fmt )

		response = render_to_response(
					ntn,
					{
						'instance' : ob,
						'extra' : extra,
						'result' : result,
					},
					context_instance=RequestContext(request)
				)

		response[ 'Content-Type' ] = self.supported_formats[ fmt ]
		return response

