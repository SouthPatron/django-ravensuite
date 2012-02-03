from __future__ import unicode_literals

from django.views.generic.base import View
from django.http import HttpResponse, Http404

import json

from django.views.decorators.csrf import csrf_exempt, csrf_protect

class Base( View ):
	template_name = None
	url_kwargs = None

	supported_formats = {
		'html' : 'text/html',
		'json' : 'application/json',
	}

	# ************** CSRF workarounds per format


	@csrf_exempt
	def dispatch(self, request, *args, **kwargs):

		self.url_kwargs = self._extract_all_kwargs( **kwargs )

		@csrf_protect
		def protected( request, *args, **kwargs ):
			return super( Base, self ).dispatch( request, *args, **kwargs )

		fmt = self._parse_format( request )

		if fmt == 'html':
			return protected( request, *args, **kwargs )

		return super( Base, self ).dispatch( request, *args, **kwargs )

	# ************** Unlikely to override

	def get_template_name( self, method, fmt ):
		if self.template_name is None:
			raise RuntimeError( 'template_name has not been defined in instance' )
		ntn = '{}.{}.{}'.format( self.template_name, method, fmt )
		return ntn
	

	# ************** Probably won't override
	
	def not_found( self ):
		raise Http404( 'Object Not Found' )


	# ************** Support methods

	def _parse_format( self, request ):
		fmt = request.GET.get( 'format', 'html' )
		if fmt not in self.supported_formats:
			return None
		return fmt

	def _get_query_data( self, request ):
		return request.GET

	def _get_body_data( self, request, fmt ):
		if fmt == 'html':
			return request.POST

		if fmt == 'json':
			data = request.read()
			if data is None or len(data) == 0:
				return {}
			return json.loads( data )

	def _extract_all_kwargs( self, **kwargs ):
		class IdObject( object ):
			pass
		myid = IdObject()
		for nm, val in kwargs.iteritems():
			setattr( myid, nm, val )
		return myid


	# ************** Response methods

	def _api_json( self, response, body ):
		encoded = json.dumps( body )
		response[ 'Content-Length' ] = len(encoded)
		response.write( encoded )
		return response


	def api_resp( self, body, form = 'json' ):
		resp = HttpResponse( mimetype = self.supported_formats[ form ], status = 200 )
		resp['Cache-Control'] = 'no-cache'

		if form == 'json':
			return self._api_json( resp, body )

		raise RuntimeError( 'No such known form: {}'.format( form ) )


