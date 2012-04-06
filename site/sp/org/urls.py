from django.contrib.auth.decorators import login_required

from django.conf.urls import url, patterns
from django.conf import settings

from views import *


from common.views.modal import ModalView


urlpatterns = patterns('',

# ------- ORGANIZATION -------------------------

	url( r'^$', login_required( OrgList.as_view() ), name = 'org-list' ),
	url( r'^(?P<oid>\w{32})$', login_required( OrgSingle.as_view() ), name = 'org-single' ),


	url( r'^(?P<oid>\w{32})/test$', login_required( OrgTestSingle.as_view() ), name = 'org-test-single' ),


# ------ SETTINGS -------------------------------


	url( r'^(?P<oid>\w{32})/admin$', login_required( AdminSingle.as_view() ), name = 'org-admin-single' ),


# ------ USERS -------------------------------


	url( r'^(?P<oid>\w{32})/admin/users$', login_required( UserList.as_view() ), name = 'org-admin-user-list' ),
	url( r'^(?P<oid>\w{32})/admin/user/(?P<uid>\d+)$', login_required( UserSingle.as_view() ), name = 'org-admin-user-single' ),



# ------ CLIENTS -----------------------------


	url( r'^(?P<oid>\w{32})/clients$', login_required( ClientList.as_view() ), name = 'org-client-list' ),


	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)$', login_required( ClientSingle.as_view() ), name = 'org-client-single' ),


# ------ CLIENTS / PROJECTS ------------------

	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/projects$', login_required( ProjectList.as_view() ), name = 'org-client-project-list' ),
	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/project/(?P<pid>\d+)$', login_required( ProjectSingle.as_view() ), name = 'org-client-project-single' ),


# ------ CLIENTS / ACCOUNT ------------------

	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account$', login_required( AccountSingle.as_view() ), name = 'org-client-account-single' ),

	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account/transactions$', login_required( AccountTransactionList.as_view() ), name = 'org-client-account-transaction-list' ),
	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account/transaction/(?P<tid>\d+)$', login_required( account_transaction_router ), name = 'org-client-account-transaction-single' ),


# ------ CLIENTS / ACCOUNT / INVOICES ------------------

	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account/transactions/invoices$', login_required( InvoiceList.as_view() ), name = 'org-client-account-transaction-invoice-list' ),
	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account/transactions/invoice/(?P<sdid>\d+)$', login_required( InvoiceSingle.as_view() ), name = 'org-client-account-transaction-invoice-single' ),


	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account/transactions/invoices/draft$', login_required( InvoiceDraftList.as_view() ), name = 'org-client-account-transaction-invoice-draft-list' ),
	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account/transactions/invoices/unpaid$', login_required( InvoiceUnpaidList.as_view() ), name = 'org-client-account-transaction-invoice-unpaid-list' ),


# ------ CLIENTS / ACCOUNT / PAYMENT ------------------

	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account/transactions/payments$', login_required( PaymentList.as_view() ), name = 'org-client-account-transaction-payment-list' ),

	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account/transactions/payments/draft$', login_required( PaymentDraftList.as_view() ), name = 'org-client-account-transaction-payment-draft-list' ),

	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account/transactions/payments/unallocated$', login_required( PaymentUnallocatedList.as_view() ), name = 'org-client-account-transaction-payment-unallocated-list' ),

	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account/transactions/payment/(?P<sdid>\d+)$', login_required( PaymentSingle.as_view() ), name = 'org-client-account-transaction-payment-single' ),


# ------ CLIENTS / ACCOUNT / CREDIT NOTES ------------------

	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account/transactions/credit-notes$', login_required( CreditNoteList.as_view() ), name = 'org-client-account-transaction-credit-note-list' ),
	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account/transactions/credit-note/(?P<sdid>\d+)$', login_required( CreditNoteSingle.as_view() ), name = 'org-client-account-transaction-credit-note-single' ),


	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account/transactions/credit-notes/draft$', login_required( CreditNoteDraftList.as_view() ), name = 'org-client-account-transaction-credit-note-draft-list' ),
	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account/transactions/credit-notes/unallocated$', login_required( CreditNoteUnallocatedList.as_view() ), name = 'org-client-account-transaction-credit-note-unallocated-list' ),



# ------ CLIENTS / ACCOUNT / REFUNDS ------------------

	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account/transactions/refunds$', login_required( RefundList.as_view() ), name = 'org-client-account-transaction-refund-list' ),

	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account/transactions/refunds/draft$', login_required( RefundDraftList.as_view() ), name = 'org-client-account-transaction-refund-draft-list' ),

	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account/transactions/refunds/unallocated$', login_required( RefundUnallocatedList.as_view() ), name = 'org-client-account-transaction-refund-unallocated-list' ),

	url( r'^(?P<oid>\w{32})/client/(?P<cid>\d+)/account/transactions/refund/(?P<sdid>\d+)$', login_required( RefundSingle.as_view() ), name = 'org-client-account-transaction-refund-single' ),


# ------ ACTIVITIES -----------------------------


	url( r'^(?P<oid>\w{32})/activities$', login_required( ActivityList.as_view() ), name = 'org-activity-list' ),
	url( r'^(?P<oid>\w{32})/activity/(?P<actid>\d+)$', login_required( ActivitySingle.as_view() ), name = 'org-activity-single' ),


	url( r'^(?P<oid>\w{32})/activity/(?P<actid>\d+)/tasks$', login_required( TaskList.as_view() ), name = 'org-activity-task-list' ),
	url( r'^(?P<oid>\w{32})/activity/(?P<actid>\d+)/task/(?P<taskid>\d+)$', login_required( TaskSingle.as_view() ), name = 'org-activity-task-single' ),


	url( r'^modals/(?P<modal_name>.*)$', login_required( ModalView.as_view() ) ),

)


