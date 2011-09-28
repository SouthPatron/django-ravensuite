from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',

	url( r'^$', OrgList.as_view(), name = 'org-list' ),
	url( r'^(?P<oid>\d+)$', OrgSingle.as_view(), name = 'org-single' ),


	url( r'^(?P<oid>\d+)/clients$', ClientList.as_view(), name = 'org-client-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)$', ClientSingle.as_view(), name = 'org-client-single' ),


	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/accounts$', AccountList.as_view(), name = 'org-client-account-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/(?P<aid>\d+)$', AccountSingle.as_view(), name = 'org-client-account-single' ),

)

