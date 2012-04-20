from __future__ import unicode_literals

from common.views.restfulview import RestfulView, RestForbidden
from common.utils.class_loader import ClassLoader

import re

from ..api_restful import restful_list



class RestfulLogic( object ):

#	class Meta:
#		allow_update = True
#		readonly = ( 'refnum', )
#		fields = ( 'trading_name', 'telephone_number', )
#		exclude = ( 'fax_number', )


	def __init__( self, view, *args, **kwargs ):
		super( RestfulLogic, self ).__init__( *args, **kwargs )
		self.view = view
		self.url_kwargs = view.url_kwargs

	def create_object( self, request, data, *args, **kwargs ):
		raise RestForbidden()

	def delete_object( self, request, *args, **kwargs ):
		raise RestForbidden()

	def get_object( self, request, *args, **kwargs ):
		return self.view.not_found()

	def update_object( self, request, data, *args, **kwargs ):
		meta = getattr( self, 'Meta', None )
		obj = self.get_object( request, *args, **kwargs )
		return self.view.def_update_object( request, data, obj, meta )


class RestfulDispatcher( RestfulView ):

	# ********* Class Members

	base_module = 'sp.api.restful'
	logic = None

	# ********* Support Methods

	def _search_match( self, request, *args, **kwargs ):
		node = kwargs[ 'node' ]
		for pair in restful_list:
			m = re.match( pair[0], node )
			if m is not None:
				return { 'args' : m.groupdict(), 'classname' : pair[1] }
		return None

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

	# ********* Parts to be dispatched to RestfulLogics

	def create_object( self, request, data, *args, **kwargs ):
		self._prepare( request, *args, **kwargs )
		return self.logic.create_object( request, data, *args, **kwargs )

	def delete_object( self, request, *args, **kwargs ):
		self._prepare( request, *args, **kwargs )
		return self.logic.delete_object( request, *args, **kwargs )

	def get_object( self, request, *args, **kwargs ):
		self._prepare( request, *args, **kwargs )
		return self.logic.get_object( request, *args, **kwargs )

	def update_object( self, request, data, *args, **kwargs ):
		self._prepare( request, *args, **kwargs )
		return self.logic.update_object( request, data, *args, **kwargs )


