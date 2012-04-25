from __future__ import unicode_literals

from common.views.pageview import *

from ..models import *

class AccountPageView( PageView ):

	def get_organization( self, request, *args, **kwargs ):
		if hasattr( self.url_kwargs, 'oid' ):
			return Organization.objects.get( refnum = self.url_kwargs.oid )
		return None

	def _preload( self, request, *args, **kwargs ):
		super( AccountPageView, self )._preload( request, *args, **kwargs )
		self.dataset[ 'organization' ] = self.get_organization( request, *args, **kwargs )

