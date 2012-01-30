from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from common.views.component import ComponentView
from common.models import *

class OrgComponents( ComponentView ):

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404(
					Organization,
					refnum = self.url_kwargs.oid,
				)

