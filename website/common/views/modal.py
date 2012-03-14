from __future__ import unicode_literals

from copy import deepcopy

from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader, TemplateDoesNotExist, RequestContext
from django.shortcuts import render_to_response, redirect
from base import Base

from common.exceptions import BLE_DevError

import inspect


class ModalLogic( object ):

	def __init__( self, kwargs ):
		self.url_kwargs = kwargs

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

	def _fetch_call( self, request, logic, modal_name, fmt, dmap, *args, **kwargs ):
		ob = logic.get_object( request, dmap, *args, **kwargs )
		if ob is None:
			raise BLE_DevError( 'None from logic.get_object' )

		extra = logic.get_extra( request, dmap, *args, **kwargs )

		context = RequestContext(
							request,
							{
								'instance' : ob,
								'extra' : extra,
								'kwargs' : self.url_kwargs,
								'data' : dmap
							}
						)
		return render_to_response(
					self.get_template_name( modal_name, "fetch", fmt ), 
					context
				)


	def _apply_call( self, request, logic, modal_name, fmt, dmap, *args, **kwargs ):
		ob = logic.get_object( request, dmap, *args, **kwargs )
		if ob is None:
			raise BLE_DevError( 'None from logic.get_object' )

		extra = logic.get_extra( request, dmap, *args, **kwargs )

		ans = logic.perform( request, dmap, ob, extra, fmt, *args, **kwargs )
		if ans is not None:
			return ans

		context = RequestContext(
							request,
							{
								'instance' : ob,
								'extra' : extra,
								'kwargs' : self.url_kwargs,
								'data' : dmap
							}
						)
		return render_to_response(
					self.get_template_name( modal_name, "apply", fmt ), 
					context
				)


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

		logic = logic_class( self.url_kwargs )

		if dmap.get( 'meta.action', 'fetch' ) == 'apply':
			return self._apply_call( request, logic, modal_name, fmt, dmap, *args, **kwargs )

		return self._fetch_call( request, logic, modal_name, fmt, dmap, *args, **kwargs )


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



