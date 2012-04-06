from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404

from common.views.singleobjectview import SingleObjectView
from common.models import *




class AdminSingle( SingleObjectView ):
	template_name = 'pages/org/admin/single'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Organization, refnum = self.url_kwargs.oid )

