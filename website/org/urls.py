from django.conf.urls.defaults import *
from django.conf import settings

from views import *

urlpatterns = patterns('',

	url( r'^$', OrgList.as_view(), name = 'org-list' ),
	url( r'^(?P<oid>\d+)$', OrgSingle.as_view(), name = 'org-single' ),


# ------ CLIENTS -----------------------------


	url( r'^(?P<oid>\d+)/clients$', ClientList.as_view(), name = 'org-client-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)$', ClientSingle.as_view(), name = 'org-client-single' ),


# ------ CLIENTS / ACCOUNTS ------------------

	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/accounts$', AccountList.as_view(), name = 'org-client-account-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/(?P<aid>\d+)$', AccountSingle.as_view(), name = 'org-client-account-single' ),


	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/(?P<aid>\d+)/transactions$', AccountTransactionList.as_view(), name = 'org-client-account-transaction-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/(?P<aid>\d+)/transaction/(?P<tid>\d+)$', AccountTransactionSingle.as_view(), name = 'org-client-account-transaction-single' ),


# ------ CLIENTS / TABS ----------------------


	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/tabs$', AccountList.as_view(), name = 'org-client-tab-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/tab/(?P<tabid>\d+)$', AccountSingle.as_view(), name = 'org-client-tab-single' ),


	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/tab/(?P<tabid>\d+)/transactions$', TabTransactionList.as_view(), name = 'org-client-tab-transaction-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/tab/(?P<tabid>\d+)/transaction/(?P<tid>\d+)$', TabTransactionSingle.as_view(), name = 'org-client-tab-transaction-single' ),

	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/tab/(?P<tabid>\d+)/reservations$', ReservationList.as_view(), name = 'org-client-tab-reservation-list' ),

	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/tab/(?P<tabid>\d+)/reservation/(?P<rid>[0-9a-fA-F]{32})$', ReservationSingle.as_view(), name = 'org-client-tab-reservation-single' ),



# ------ CLIENTS / INVOICES ------------------

	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/(?P<aid>\d+)/invoices$', InvoiceList.as_view(), name = 'org-client-account-invoice-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/(?P<aid>\d+)/invoice/(?P<iid>\d+)$', InvoiceSingle.as_view(), name = 'org-client-account-invoice-single' ),


)


