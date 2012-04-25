from django.shortcuts import get_object_or_404

from account.views import AccountPageView
from common.models import *


class ActivityList( AccountPageView ):
	template_name = 'pages/org/activity/index'

	def get_object( self, request, *args, **kwargs ):
		return Organization.objects.get( refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = Activity.objects.filter( organization__refnum = self.url_kwargs.oid )
		return obj_list


class ActivitySingle( AccountPageView ):
	template_name = 'pages/org/activity/single'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Activity, id = self.url_kwargs.actid, organization__refnum = self.url_kwargs.oid )

