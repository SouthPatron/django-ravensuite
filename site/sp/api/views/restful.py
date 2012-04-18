from __future__ import unicode_literals

from django.template import RequestContext
from django.shortcuts import render_to_response

from common.views.restfulview import RestfulView, RestForbidden

from common.utils.class_loader import ClassLoader

import logging
import re

logger = logging.getLogger( __name__ )

from ..api_restful import restful_list



class RestfulLogic( object ):
	def __init__( self, view, *args, **kwargs ):
		super( RestfulLogic, self ).__init__( *args, **kwargs )
		self.view = view
		self.dataset = view.dataset
		self.kwargs = self.dataset[ 'kwargs' ]

	def create_object( self, request, data, *args, **kwargs ):
		raise RestForbidden()

	def delete_object( self, request, *args, **kwargs ):
		raise RestForbidden()

	def get_extra( self, request, *args, **kwargs ):
		return None

	def get_object( self, request, *args, **kwargs ):
		return None

	def get_object_list( self, request, *args, **kwargs ):
		return None
	
	def update_object( self, request, data, *args, **kwargs ):
		raise RestForbidden()



class RestfulDispatcher( RestfulView ):

	# ********* Class Members

	base_module = 'sp.api.restful'
	base_template = 'api.restful'
	logic = None

	# ********* Support Methods

	def _search_match( self, request, *args, **kwargs ):
		node = kwargs[ 'node' ]
		for pair in restful_list:
			m = re.match( pair[0], node )
			if m is not None:
				return { 'args' : m.groupdict(), 'classname' : pair[1] }
		return None

	def _create_template_name( self, stubname ):
		full_path = '{}.{}'.format( self.base_template, stubname )
		parts = full_path.split('.')
		return '/'.join( parts )

	def _prepare( self, request, *args, **kwargs ):
		if self.logic is not None:
			return

		match = self._search_match( request, *args, **kwargs )
		if match is None:
			return self.not_found()

		# Append new args to self.url_kwargs
		for nm, val in match[ 'args' ].iteritems():
			setattr( self.url_kwargs, nm, val )

		# Instantiate the logic class
		logic = ClassLoader.load( '{}.{}'.format( self.base_module, match['classname'] ) )
		if logic is None:
			return self.not_found()
		self.logic = logic( self )

		# Generate template name
		self.template_name = self._create_template_name( match['classname'] )

	# ********* Parts to be dispatched to RestfulLogics

	def create_object( self, request, data, *args, **kwargs ):
		self._prepare( request, *args, **kwargs )
		return self.logic.create_object( request, data, *args, **kwargs )

	def delete_object( self, request, *args, **kwargs ):
		self._prepare( request, *args, **kwargs )
		return self.logic.delete_object( request, *args, **kwargs )

	def get_extra( self, request, *args, **kwargs ):
		self._prepare( request, *args, **kwargs )
		return self.logic.get_extra( request, *args, **kwargs )

	def get_object( self, request, *args, **kwargs ):
		self._prepare( request, *args, **kwargs )
		return self.logic.get_object( request, *args, **kwargs )

	def get_object_list( self, request, *args, **kwargs ):
		self._prepare( request, *args, **kwargs )
		return self.logic.get_object_list( request, *args, **kwargs )
	
	def update_object( self, request, data, *args, **kwargs ):
		return self.logic.update_object( request, data, *args, **kwargs )





