from django.shortcuts import get_object_or_404, redirect

from common.views.pageview import PageView
from common.models import *


class UserList( PageView ):
	template_name = 'pages/org/admin/user/index'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Organization, refnum = self.url_kwargs.oid )

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = UserMembership.objects.filter( organization__refnum = self.url_kwargs.oid )
		return obj_list


class UserSingle( PageView ):
	template_name = 'pages/org/admin/user/single'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( UserMembership, id = self.url_kwargs.uid, organization__refnum = self.url_kwargs.oid )


