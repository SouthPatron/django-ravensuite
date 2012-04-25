from django.shortcuts import get_object_or_404

from account.views import AccountPageView
from common.models import *


class AccountSingle( AccountPageView ):
	template_name = 'pages/org/client/account/single'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Account, client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid )

