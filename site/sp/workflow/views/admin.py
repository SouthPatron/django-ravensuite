from django.shortcuts import get_object_or_404

from account.views import AccountPageView
from common.models import *


class AdminSingle( AccountPageView ):
	template_name = 'pages/org/admin/single'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Organization, refnum = self.url_kwargs.oid )

