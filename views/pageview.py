from __future__ import unicode_literals

from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.views.generic.base import View
from django.http import Http404

class PageForbidden( Exception ):
	pass

class PageResponse( Exception ):
	def __init__( self, response, *args, **kwargs ):
		self.response = response
		super( PageResponse, self ).__init__( *args, **kwargs )

class PageRender( Exception ):
	def __init__( self, result = None, *args, **kwargs ):
		self.result = result
		super( PageRender, self ).__init__( *args, **kwargs )

class PageView( View ):

	# ************** Class Members

	template_name = None
	url_kwargs = None

	# ************** Probably want to override

	def get_extra( self, request, *args, **kwargs ):
		return None

	def get_object( self, request, *args, **kwargs ):
		return None

	def get_object_list( self, request, *args, **kwargs ):
		return None
	
	def update_object( self, request, data, *args, **kwargs ):
		raise PageForbidden()

	# ************** Initialization, Gathering & Dispatching

	def _preload( self, request, *args, **kwargs ):
		self.dataset = {
				'kwargs' : self.url_kwargs,
				'object_list' : self.get_object_list( request, *args, **kwargs ),
				'instance' : self.get_object( request, *args, **kwargs ),
				'extra' : self.get_extra( request, *args, **kwargs ),
				'result' : None,
			}

	def dispatch( self, request, *args, **kwargs ):

		# Load all the kwargs into a local attribute
		class IdObject( object ):
			pass
		self.url_kwargs = IdObject()
		for nm, val in kwargs.iteritems():
			setattr( self.url_kwargs, nm, val )

		self._preload( request, *args, **kwargs )

		try:
			return super( PageView, self ).dispatch( request, *args, **kwargs )
		except PageForbidden:
			return HttpResponseForbidden()
		except PageResponse, pd:
			return pd.response


	# ************** Support Methods

	def get_template_name( self, method ):
		if self.template_name is None:
			raise RuntimeError( 'template_name not yet set' )
		return '{}.{}.html'.format( self.template_name, method )

	def not_found( self ):
		raise Http404( 'Object Not Found' )

	# ************** HTTP Operations

	def get( self, request, *args, **kwargs ):
		ntn = self.get_template_name( 'get' )
		return render_to_response(
					ntn,
					self.dataset,
					context_instance=RequestContext( request )
				)

	def post( self, request, *args, **kwargs ):
		data = request.POST or {}

		try:
			return self.update_object( request, data, *args, **kwargs )
		except PageRender, pr:
			self.dataset[ 'result' ] = pr.result
			ntn = self.get_template_name( 'post' )
			return render_to_response(
					ntn,
					self.dataset,
					context_instance=RequestContext( request )
				)


