from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from common.views.singleobjectview import SingleObjectView

from common.models import *
from common.buslog.org import *
from common.exceptions import *


class AccountSingle( SingleObjectView ):
	template_name = 'pages/org/client/account/single'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Account, client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid )



