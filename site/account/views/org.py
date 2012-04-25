from pageview import AccountPageView
from ..models import *


class OrgList( AccountPageView ):
	template_name = 'pages/account/org_index'

	def get_object_list( self, request, *args, **kwargs ):
		return Organization.objects.filter( profile = request.user.get_profile() )

class OrgSingle( AccountPageView ):
	template_name = 'pages/account/org_single'

	def get_object( self, request, *args, **kwargs ):
		return Organization.objects.get( refnum = self.url_kwargs.oid )


