from __future__ import unicode_literals

from copy import deepcopy

from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader, TemplateDoesNotExist, RequestContext
from base import Base

import mimetypes

#
#  _current_page
#  _action
#
#  Everything else.
#


class ComponentView( Base ):

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


	def get_delivery_component( self, request, page, data, context ):
		part = request.GET.get( 'part', 'html' )
		suffix = self.part_mapping[ part ]
		fname = '{}.{}.{}'.format( self.template_name, page, suffix )

		try:
			t = loader.get_template( fname )
			body = t.render( context )
		except TemplateDoesNotExist:
			if part == 'html':
				return None
			body = ''

		return HttpResponse(
						body,
						mimetype = mimetypes.guess_type( fname )[0]
					)

	# ************** Thunking operation

	def _verify_call( self, request, fmt, ob, extra, data, *args, **kwargs ):
		handler = getattr( self, 'verify_{}'.format( fmt ), None )
		if handler is None:
			return None

		return handler( request, ob, extra, data, *args, **kwargs )

	def _post_call( self, request, fmt, ob, extra, data, *args, **kwargs ):
		handler = getattr( self, 'post_{}'.format( fmt ), None )
		if handler is None:
			return HttpResponseForbidden()

		return handler( request, ob, extra, data, *args, **kwargs )


	def _prepare_data( self, request, fmt ):
		data = self._get_body_data( request, fmt )

		if data is None:
			data = { '_page' : 1 }

		data = deepcopy( data )

		query_data = self._get_query_data( request )

		if query_data is not None:
			data.update( query_data )

		if '_page' not in data:
			data[ '_page' ] = 1

		data[ '_page' ] = long( data[ '_page' ] )
		return data


	def _thunk( self, request, *args, **kwargs ):
		fmt = self._parse_format( request )
		if fmt is None: return HttpResponseForbidden()

		ob = self.get_object( request, *args, **kwargs )
		if ob is None: self.not_found()

		extra = self.get_extra( request, ob, fmt, *args, **kwargs )

		data = self._prepare_data( request, fmt )

		context = RequestContext(
							request,
							{
								'instance' : ob,
								'extra' : extra,
								'kwargs' : self.url_kwargs,
								'data' : data
							}
						)

		pc = self._verify_call(
						request,
						fmt,
						ob,
						extra,
						data,
						*args,
						**kwargs
					)
		if pc is not None:
			return pc

		rc = self.get_delivery_component(
					request,
					data[ '_page' ],
					data,
					context
				)

		if rc is None:
			rc = self._post_call(
						request,
						fmt,
						ob,
						extra,
						data,
						*args,
						**kwargs
					)

		return rc


	# ************** HTTP Operations

	def get( self, request, *args, **kwargs ):
		return self._thunk( request, *args, **kwargs )

	def post( self, request, *args, **kwargs ):
		return self._thunk( request, *args, **kwargs )



