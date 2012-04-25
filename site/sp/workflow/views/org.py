from django.shortcuts import get_object_or_404, redirect
from account.views import AccountPageView
from common.models import *


class OrgList( AccountPageView ):
	template_name = 'pages/org/index'

	def get_object_list( self, request, *args, **kwargs ):
		umems = UserMembership.objects.filter( user = request.user )

		newobj_list = []
		for obj in umems:
			org = obj.organization
			org.membership = obj
			newobj_list.append( org )

		return newobj_list

class OrgSingle( AccountPageView ):
	template_name = 'pages/org/single'

	def get_object( self, request, *args, **kwargs ):
		return get_object_or_404( Organization, refnum = self.url_kwargs.oid )


class OrgTestSingle( AccountPageView ):
	template_name = 'pages/org/test'

	def get_object( self, request, *args, **kwargs ):
		return { 'hello' : True }



