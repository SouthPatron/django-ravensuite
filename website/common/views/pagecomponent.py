from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader, TemplateDoesNotExist, RequestContext
from base import Base

import mimetypes

class PageComponentView( Base ):

	# ************** Mapping

	part_mapping = {
			'javascript' : 'js',
			'stylesheet' : 'css',
			'html' : 'html',
		}

	# ************** Probably want to override

	def get_extra( self, request, *args, **kwargs ):
		return None

	def get_object( self, request, *args, **kwargs ):
		return None


	# ************** Support methods

	def _process_dc( self, fname, context ):
		try:
			t = loader.get_template( fname )
			return t.render( context )
		except TemplateDoesNotExist:
			return ''


	def get_delivery_name( self, request ):
		part = request.GET.get( 'part', 'html' )
		suffix = self.part_mapping[ part ]
		return '{}.{}'.format( self.template_name, suffix )
		

	def get_delivery_component( self, request, context ):
		fname = self.get_delivery_name( request )
		response = HttpResponse(
						self._process_dc( fname, context ),
						mimetype = mimetypes.guess_type( fname )[0]
					)
		return response
		
		

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

		return self.get_delivery_component( request, context )


