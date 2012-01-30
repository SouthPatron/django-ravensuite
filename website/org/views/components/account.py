from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from common.views.component import ComponentView
from common.models import *


class AccountComponents( ComponentView ):

	def get_extra( self, request, *args, **kwargs ):
		return get_object_or_404(
					Client,
					refnum = self.url_kwargs.cid,
					organization__refnum = self.url_kwargs.oid
				)

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404(
					Account,
					client__refnum = self.url_kwargs.cid,
					client__organization__refnum = self.url_kwargs.oid
				)

