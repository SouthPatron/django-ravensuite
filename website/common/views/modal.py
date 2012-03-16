from __future__ import unicode_literals

from django.http import HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import render_to_response
from base import Base

import inspect


class ModalLogic( object ):

	class Easy( object ):
		def __init__( self, parent ):
			super( ModalLogic.Easy, self ).__init__()
			self.parent = parent

		def redirect( self ):
			self.parent.template_name = 'modals/_common/redirect.{}.{}'.format( self.parent.method, self.parent.fmt )

		def notice( self ):
			self.parent.template_name = 'modals/_common/notice.{}.{}'.format( self.parent.method, self.parent.fmt )

		def make_get( self ):
			self.parent.method = 'get'

		def make_post( self ):
			self.parent.method = 'post'


	def __init__( self, request, fmt, kwargs ):
		super( ModalLogic, self ).__init__()
		self.url_kwargs = kwargs
		self.method = request.method.lower()
		self.fmt = fmt
		self.template_name = None
		self.easy = ModalLogic.Easy( self )

	def prepare( self, *args, **kwargs ):
		pass

	def get_extra( self, request, dmap, *args, **kwargs ):
		return None

	def get_object( self, request, dmap, *args, **kwargs ):
		return None

	def perform( self, request, dmap, obj, extra, fmt, *args, **kwargs ):
		return None


class ModalView( Base ):

	# ************** Support methods

	def _expand_modal_name( self, modal_name ):
		return '{}'.format( '/'.join( modal_name.split( '.' ) ) )

	def get_template_name( self, modal_name, action, fmt ):
		return 'modals/{}.{}.{}'.format(
					self._expand_modal_name( modal_name ),
					action,
					fmt
				),

	# ************** Thunking operation


	def _load_class( self, modal_name ):
		parts = modal_name.split('.')
		parts.insert( 1, 'modals' )
		module = ".".join(parts[0:2])

		classname = ""
		for mystr in parts[2:]:
			classname = "{}{}".format( classname, mystr.capitalize() )

		try:
			m = __import__( module )
			for comp in parts[1:2]:
				m = getattr(m, comp)

			m = getattr(m, classname )
		except AttributeError:
			return None

		return m


	def _thunk( self, request, modal_name, fmt, dmap, *args, **kwargs ):

		logic_class = self._load_class( modal_name )
		if logic_class is None:
			return self.not_found()

		logic = logic_class( request, fmt, self.url_kwargs )
		logic.prepare( request, modal_name, fmt, dmap, *args, **kwargs )

		ob = logic.get_object( request, dmap, *args, **kwargs )
		extra = logic.get_extra( request, dmap, *args, **kwargs )

		if request.method == 'POST':
			result = logic.perform( request, dmap, ob, extra, fmt, *args, **kwargs )
		else:
			result = None

		template_name = logic.template_name or self.get_template_name(
								modal_name,
								logic.method or request.method.lower(),
								fmt
							)

		context = RequestContext(
							request,
							{
								'instance' : ob,
								'extra' : extra,
								'kwargs' : self.url_kwargs,
								'data' : dmap,
								'result' : result
							}
						)
		return render_to_response( template_name, context )


	# ************** HTTP Operations

	def get( self, request, modal_name, *args, **kwargs ):
		fmt = self._parse_format( request )
		if fmt is None: return HttpResponseForbidden()

		dmap = self._get_query_data( request )
		return self._thunk( request, modal_name, fmt, dmap, *args, **kwargs )

	def post( self, request, modal_name, *args, **kwargs ):
		fmt = self._parse_format( request )
		if fmt is None: return HttpResponseForbidden()

		dmap = self._get_body_data( request, fmt )
		return self._thunk( request, modal_name, fmt, dmap, *args, **kwargs )



