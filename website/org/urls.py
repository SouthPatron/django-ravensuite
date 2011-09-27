from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',

	url(
		r'^$',
		OrgList.as_view(),
		{
		},
		name = 'org-list' ),

	url(
		r'^(?P<oid>\d+)$',
		OrgSingle.as_view(),
		{ 
		},
		name = 'org-single',
	),

)

