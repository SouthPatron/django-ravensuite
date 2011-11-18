from django.contrib.auth.decorators import login_required

from django.conf.urls.defaults import *
from django.conf import settings

from views import *

urlpatterns = patterns('',

	url( r'^$', login_required( OrgList.as_view() ), name = 'org-list' ),
	url( r'^(?P<oid>\d+)$', login_required( OrgSingle.as_view() ), name = 'org-single' ),


# ------ CLIENTS -----------------------------


	url( r'^(?P<oid>\d+)/clients$', login_required( ClientList.as_view() ), name = 'org-client-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)$', login_required( ClientSingle.as_view() ), name = 'org-client-single' ),


# ------ CLIENTS / ACCOUNTS ------------------

	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/accounts$', login_required( AccountList.as_view() ), name = 'org-client-account-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/(?P<aid>\d+)$', login_required( AccountSingle.as_view() ), name = 'org-client-account-single' ),


	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/(?P<aid>\d+)/transactions$', login_required( AccountTransactionList.as_view() ), name = 'org-client-account-transaction-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/(?P<aid>\d+)/transaction/(?P<tid>\d+)$', login_required( AccountTransactionSingle.as_view() ), name = 'org-client-account-transaction-single' ),


# ------ CLIENTS / TABS ----------------------


	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/tabs$', login_required( TabList.as_view() ), name = 'org-client-tab-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/tab/(?P<tabid>\d+)$', login_required( TabSingle.as_view() ), name = 'org-client-tab-single' ),


	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/tab/(?P<tabid>\d+)/transactions$', login_required( TabTransactionList.as_view() ), name = 'org-client-tab-transaction-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/tab/(?P<tabid>\d+)/transaction/(?P<tid>\d+)$', login_required( TabTransactionSingle.as_view() ), name = 'org-client-tab-transaction-single' ),

	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/tab/(?P<tabid>\d+)/reservations$', login_required( ReservationList.as_view() ), name = 'org-client-tab-reservation-list' ),

	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/tab/(?P<tabid>\d+)/reservation/(?P<rid>[0-9a-fA-F]{32})$', login_required( ReservationSingle.as_view() ), name = 'org-client-tab-reservation-single' ),



# ------ CLIENTS / INVOICES ------------------

	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/(?P<aid>\d+)/invoices$', login_required( InvoiceList.as_view() ), name = 'org-client-account-invoice-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/(?P<aid>\d+)/invoice/(?P<iid>\d+)$', login_required( InvoiceSingle.as_view() ), name = 'org-client-account-invoice-single' ),


# ------ ACTIVITIES -----------------------------


	url( r'^(?P<oid>\d+)/activities$', login_required( ActivityList.as_view() ), name = 'org-activity-list' ),
	url( r'^(?P<oid>\d+)/activity/(?P<actid>\d+)$', login_required( ActivitySingle.as_view() ), name = 'org-activity-single' ),


	url( r'^(?P<oid>\d+)/activity/(?P<actid>\d+)/tasks$', login_required( TaskList.as_view() ), name = 'org-activity-task-list' ),
	url( r'^(?P<oid>\d+)/activity/(?P<actid>\d+)/task/(?P<taskid>\d+)$', login_required( TaskSingle.as_view() ), name = 'org-activity-task-single' ),


)


