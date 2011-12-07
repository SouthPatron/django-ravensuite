from __future__ import unicode_literals

from django.http import HttpResponseForbidden
from django.template import loader, RequestContext
from base import Base

class PageComponentView( Base ):

	# ************** Probably want to override

	javascript = None
	stylesheet = None
	html = None

	def get_extra( self, request, *args, **kwargs ):
		return None

	def get_object( self, request, *args, **kwargs ):
		return None


	# ************** Support methods

	def _get_dc( self, suffix, attr ):
		if attr is not None:
			return attr

		if self.template_name is None:
			return None

		return [ '{}.{}'.format( self.template_name, suffix ) ]


	def _process_dc( self, flist, context  ):
		tresponse = []
		for fname in flist:
			t = loader.get_template( fname )
			tresponse.append( t.render( context ) )
		return tresponse


	def get_delivery_components( self, context, *args, **kwargs ):
		dcfiles = { 
			'javascript' : self._get_dc( 'js', self.javascript ),
			'stylesheet' : self._get_dc( 'css', self.stylesheet ),
			'html' : self._get_dc( 'html', self.html ),
		}

		dc = {
			'javascript' : self._process_dc( dcfiles['javascript'], context ),
			'stylesheet' : self._process_dc( dcfiles['stylesheet'], context ),
			'html' : self._process_dc( dcfiles['html'], context ),
		}
		return dc

		

	# ************** HTTP Operations

	def get( self, request, *args, **kwargs ):
		fmt = self._parse_format( request )
		if fmt is None: return HttpResponseForbidden()

		ob = self.get_object( request, *args, **kwargs )
		if ob is None:
			self.not_found()

		extra = self.get_extra( request, ob, fmt, *args, **kwargs )

		context = RequestContext(
							request,
							{
								'instance' : ob,
								'extra' : extra,
								'kwargs' : self.url_kwargs,
							}
						)

		components = self.get_delivery_components( context )
		return self.api_resp( components, form = 'json' )


