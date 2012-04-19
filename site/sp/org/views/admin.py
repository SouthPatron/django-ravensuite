from django.shortcuts import get_object_or_404

from common.views.pageview import PageView
from common.models import *


class AdminSingle( PageView ):
	template_name = 'pages/org/admin/single'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Organization, refnum = self.url_kwargs.oid )

