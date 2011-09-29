from django.conf.urls.defaults import *
from django.conf import settings

from views import *

urlpatterns = patterns('',

	url( r'^$', OrgList.as_view(), name = 'org-list' ),
	url( r'^(?P<oid>\d+)$', OrgSingle.as_view(), name = 'org-single' ),


	url( r'^(?P<oid>\d+)/clients$', ClientList.as_view(), name = 'org-client-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)$', ClientSingle.as_view(), name = 'org-client-single' ),


	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/accounts$', AccountList.as_view(), name = 'org-client-account-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/(?P<aid>\d+)$', AccountSingle.as_view(), name = 'org-client-account-single' ),


	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/(?P<aid>\d+)/transactions$', TransactionList.as_view(), name = 'org-client-account-transaction-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/(?P<aid>\d+)/transaction/(?P<tid>\d+)$', TransactionSingle.as_view(), name = 'org-client-account-transaction-single' ),

	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/(?P<aid>\d+)/reservations$', ReservationList.as_view(), name = 'org-client-account-reservation-list' ),

)

if settings.DEBUG is True:
	urlpatterns += patterns( '',
		url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/(?P<aid>\d+)/reservation/(?P<rid>.+)$', ReservationSingle.as_view(), name = 'org-client-account-reservation-single' ),
	)
else:
	urlpatterns += patterns( '',
		url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/(?P<aid>\d+)/reservation/(?P<rid>[0-9a-fA-F]{32})$', ReservationSingle.as_view(), name = 'org-client-account-reservation-single' ),
	)
