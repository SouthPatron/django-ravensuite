from __future__ import unicode_literals

from django.views.generic.base import View
from django.http import Http404

import json

from django.views.decorators.csrf import csrf_exempt, csrf_protect

class Base( View ):
	template_name = None
	url_kwargs = None

	supported_formats = {
		'html' : 'text/html',
		'json' : 'text/json',
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

	def _get_body_data( self, request, fmt ):
		if fmt == 'html':
			return request.POST

		if fmt == 'json':
			return json.loads( request.read() )

	def _extract_all_kwargs( self, **kwargs ):
		class IdObject( object ):
			pass
		myid = IdObject()
		for nm, val in kwargs.iteritems():
			setattr( myid, nm, val )
		return myid


	def _extract_ids( self, required, **kwargs ):
		class IdObject( object ):
			pass
		myid = IdObject()
		for nm in required:
			nid = kwargs.pop( nm, None )
			if nid is None:
				self.not_found()
			setattr( myid, nm, nid )
		return myid


