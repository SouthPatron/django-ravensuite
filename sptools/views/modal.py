from __future__ import unicode_literals

from django.views.generic.base import View
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from sptools.utils.class_loader import ClassLoader


class ModalLogic( object ):

	class Easy( object ):
		def __init__( self, parent ):
			super( ModalLogic.Easy, self ).__init__()
			self.parent = parent

		def _makename( self, name ):
			self.parent.template_name = 'modals/_common/standard/{}.{}.html'.format( name, self.parent.method )

		def redirect( self ):
			self._makename( 'redirect' )

		def refresh( self ):
			self._makename( 'refresh' )

		def notice( self ):
			self._makename( 'notice' )

		def confirm( self ):
			self._makename( 'confirm' )

		def make_get( self ):
			self.parent.method = 'get'

		def make_post( self ):
			self.parent.method = 'post'


	def __init__( self, request, kwargs ):
		super( ModalLogic, self ).__init__()
		self.url_kwargs = kwargs
		self.method = request.method.lower()
		self.template_name = None
		self.easy = ModalLogic.Easy( self )

	def prepare( self, *args, **kwargs ):
		pass

	def get_extra( self, request, dmap, obj, *args, **kwargs ):
		return None

	def get_object( self, request, dmap, *args, **kwargs ):
		return None

	def get( self, request, dmap, obj, extra, *args, **kwargs ):
		return None

	def perform( self, request, dmap, obj, extra, *args, **kwargs ):
		return None


class ModalView( View ):

	url_kwargs = None

	# ************** CSRF workarounds per format

	def dispatch(self, request, *args, **kwargs):

		# Get all the URL Keywords
		class IdObject( object ):
			pass
		self.url_kwargs = IdObject()
		for nm, val in kwargs.iteritems():
			setattr( self.url_kwargs, nm, val )

		return super( ModalView, self ).dispatch( request, *args, **kwargs )

	# ************** Probably won't override

	def not_found( self ):
		raise Http404( 'Object Not Found' )

	# ************** Support methods

	def get_template_name( self, modal_name, action ):
		return 'modals/{}.{}.html'.format(
					'/'.join( modal_name.split( '.' ) ),
					action
				),

	# ************** Thunking operation

	def _thunk( self, request, modal_name, dmap, *args, **kwargs ):
		# TODO: This is hardcoded for SP module. So maybe work it out.
		parts = modal_name.split('.')
		parts.insert( 0, 'sp' )
		parts.insert( 2, 'modals' )
		full_modal_path = '.'.join( parts )

		logic_class = ClassLoader.load( full_modal_path )
		if logic_class is None:
			return self.not_found()

		logic = logic_class( request, self.url_kwargs )
		logic.prepare( request, modal_name, dmap, *args, **kwargs )

		ob = logic.get_object( request, dmap, *args, **kwargs )
		extra = logic.get_extra( request, dmap, ob, *args, **kwargs )

		if request.method == 'POST':
			result = logic.perform( request, dmap, ob, extra, *args, **kwargs )
		else:
			result = logic.get( request, dmap, ob, extra, *args, **kwargs )

		template_name = logic.template_name or self.get_template_name(
								modal_name,
								logic.method or request.method.lower()
							)

		try:
			additional = logic.additional
		except AttributeError:
			additional = None

		context = RequestContext(
							request,
							{
								'instance' : ob,
								'extra' : extra,
								'kwargs' : self.url_kwargs,
								'data' : dmap,
								'result' : result,
								'additional' : additional
							}
						)
		response = render_to_response( template_name, context )
		return response


	# ************** HTTP Operations

	def get( self, request, modal_name, *args, **kwargs ):
		dmap = request.GET or {}
		return self._thunk( request, modal_name, dmap, *args, **kwargs )

	def post( self, request, modal_name, *args, **kwargs ):
		dmap = request.POST or {}
		return self._thunk( request, modal_name, dmap, *args, **kwargs )



