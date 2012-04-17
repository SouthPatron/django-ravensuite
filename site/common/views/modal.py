from __future__ import unicode_literals

from django.http import HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import render_to_response
from base import Base

import inspect

import logging

logger = logging.getLogger( __name__ )



class ModalLogic( object ):

	class Easy( object ):
		def __init__( self, parent ):
			super( ModalLogic.Easy, self ).__init__()
			self.parent = parent

		def _makename( self, name ):
			self.parent.template_name = 'modals/_common/standard/{}.{}.{}'.format( name, self.parent.method, self.parent.fmt )

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


	def __init__( self, request, fmt, kwargs ):
		super( ModalLogic, self ).__init__()
		self.url_kwargs = kwargs
		self.method = request.method.lower()
		self.fmt = fmt
		self.template_name = None
		self.easy = ModalLogic.Easy( self )

	def prepare( self, *args, **kwargs ):
		pass

	def get_extra( self, request, dmap, obj, *args, **kwargs ):
		return None

	def get_object( self, request, dmap, *args, **kwargs ):
		return None

	def get( self, request, dmap, obj, extra, fmt, *args, **kwargs ):
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
		""" Loads a class from a modal name.

		So, takes "sp.org.modals.new.organization" ...

		Splits it by .'s

		Loads each module at a time until the attribute isn't found.
		Takes the leftover components, makes a capitalized name out
		of it and tries to load the class.

		sp.org.modals.new.organization

		with

		sp/org/modals/ with NewOrganization in namespace

		"""
		parts = modal_name.split('.')

		try:
			m = __import__( parts[0] )
			del parts[0]
		except ImportError:
			return None

		try:
			while len( parts ) > 0:
				m = getattr( m, parts[0] )
				del parts[0]
		except AttributeError:
			pass

		classname = ""
		for mystr in parts:
			classname = "{}{}".format( classname, mystr.capitalize() )

		try:
			m = getattr( m, classname )
		except AttributeError:
			logger.warning( 'unable to load class {}'.format( classname ) )
			return None

		return m


	def _thunk( self, request, modal_name, fmt, dmap, *args, **kwargs ):
		# TODO: This is hardcoded for SP module. So maybe work it out.
		parts = modal_name.split('.')
		parts.insert( 0, 'sp' )
		parts.insert( 2, 'modals' )
		full_modal_path = '.'.join( parts )

		logic_class = self._load_class( full_modal_path )
		if logic_class is None:
			return self.not_found()

		logic = logic_class( request, fmt, self.url_kwargs )
		logic.prepare( request, modal_name, fmt, dmap, *args, **kwargs )

		ob = logic.get_object( request, dmap, *args, **kwargs )
		extra = logic.get_extra( request, dmap, ob, *args, **kwargs )

		if request.method == 'POST':
			result = logic.perform( request, dmap, ob, extra, fmt, *args, **kwargs )
		else:
			result = logic.get( request, dmap, ob, extra, fmt, *args, **kwargs )

		template_name = logic.template_name or self.get_template_name(
								modal_name,
								logic.method or request.method.lower(),
								fmt
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
		response[ 'Content-Type' ] = self.supported_formats[ fmt ]
		return response


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



