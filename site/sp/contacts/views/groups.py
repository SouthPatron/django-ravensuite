from django.shortcuts import get_object_or_404, redirect

from account.views import AccountPageView

from sp.contacts import models


class GroupList( AccountPageView ):
	template_name = 'pages/contacts/groups/index'

	def get_object_list( self, request, *args, **kwargs ):
		return models.Contact.objects.filter( link__organization__refnum = self.url_kwargs.oid )


