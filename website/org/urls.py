from django.contrib.auth.decorators import login_required

from django.conf.urls.defaults import *
from django.conf import settings

from views import *


urlpatterns = patterns('',

# ------- ORGANIZATION -------------------------

	url( r'^$', login_required( OrgList.as_view() ), name = 'org-list' ),
	url( r'^(?P<oid>\d+)$', login_required( OrgSingle.as_view() ), name = 'org-single' ),


	url(
			r'^(?P<oid>\d+)/clients.pc.add_new_client$',
			login_required(
				OrgComponents.as_view(
					template_name = 'components/org/client/add_new_client'
				)
			),
			name = 'org-component-add-new-client'
		),



	url( r'^(?P<oid>\d+)/test$', login_required( OrgTestSingle.as_view() ), name = 'org-test-single' ),

# ------ USERS -------------------------------


	url( r'^(?P<oid>\d+)/users$', login_required( UserList.as_view() ), name = 'org-user-list' ),
	url( r'^(?P<oid>\d+)/user/(?P<uid>\d+)$', login_required( UserSingle.as_view() ), name = 'org-user-single' ),



# ------ CLIENTS -----------------------------


	url( r'^(?P<oid>\d+)/clients$', login_required( ClientList.as_view() ), name = 'org-client-list' ),


	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)$', login_required( ClientSingle.as_view() ), name = 'org-client-single' ),


# ------ CLIENTS / PROJECTS ------------------

	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/projects$', login_required( ProjectList.as_view() ), name = 'org-client-project-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/project/(?P<pid>\d+)$', login_required( ProjectSingle.as_view() ), name = 'org-client-project-single' ),


# ------ CLIENTS / ACCOUNT ------------------

	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account$', login_required( AccountSingle.as_view() ), name = 'org-client-account-single' ),

	url( 
			r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account.pc.receive-payment$',
			login_required(
				AccountComponents.as_view(
					template_name = 'components/org/account/receive_payment'
				)
			),
			name = 'org-client-account-component-receive-payment'
		),

	url( 
			r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account.pc.refund$',
			login_required(
				AccountComponents.as_view(
					template_name = 'components/org/account/refund'
				)
			),
			name = 'org-client-account-component-refund'
		),


	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/transactions$', login_required( AccountTransactionList.as_view() ), name = 'org-client-account-transaction-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/transaction/(?P<tid>\d+)$', login_required( account_transaction_router ), name = 'org-client-account-transaction-single' ),


# ------ CLIENTS / ACCOUNT / INVOICES ------------------

	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/invoices$', login_required( InvoiceList.as_view() ), name = 'org-client-account-invoice-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/invoice/(?P<sdid>\d+)$', login_required( InvoiceSingle.as_view() ), name = 'org-client-account-invoice-single' ),

	url( 
			r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/invoice/(?P<sdid>\d+).pc.allocate-payment$',
			login_required( IcAllocatePayment.as_view() ),
			name = 'org-client-account-invoice-component-allocate-payment'
		),

	url( 
			r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/invoice/(?P<sdid>\d+).pc.deallocate-payment$',
			login_required( IcDeallocatePayment.as_view() ),
			name = 'org-client-account-invoice-component-deallocate-payment'
		),



	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/invoices/draft$', login_required( InvoiceDraftList.as_view() ), name = 'org-client-account-invoice-draft-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/invoices/unpaid$', login_required( InvoiceUnpaidList.as_view() ), name = 'org-client-account-invoice-unpaid-list' ),


# ------ CLIENTS / ACCOUNT / PAYMENT ------------------

	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/payments$', login_required( PaymentList.as_view() ), name = 'org-client-account-payment-list' ),

	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/payments/draft$', login_required( PaymentDraftList.as_view() ), name = 'org-client-account-payment-draft-list' ),

	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/payments/unallocated$', login_required( PaymentUnallocatedList.as_view() ), name = 'org-client-account-payment-unallocated-list' ),

	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/payment/(?P<sdid>\d+)$', login_required( PaymentSingle.as_view() ), name = 'org-client-account-payment-single' ),

	url( 
			r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/payment/(?P<sdid>\d+).pc.allocate-payment$',
			login_required( PcAllocatePayment.as_view() ),
			name = 'org-client-account-payment-component-allocate-payment'
		),

	url( 
			r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/payment/(?P<sdid>\d+)/allocation/(?P<alocid>\d+)',
			login_required( PcDeallocatePayment.as_view() ),
			name = 'org-client-account-payment-component-deallocate-payment'
		),


# ------ CLIENTS / ACCOUNT / CREDIT NOTES ------------------

	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/credit-notes$', login_required( CreditNoteList.as_view() ), name = 'org-client-account-credit-note-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/credit-note/(?P<sdid>\d+)$', login_required( CreditNoteSingle.as_view() ), name = 'org-client-account-credit-note-single' ),


	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/credit-notes/draft$', login_required( CreditNoteDraftList.as_view() ), name = 'org-client-account-credit-note-draft-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/credit-notes/unallocated$', login_required( CreditNoteUnallocatedList.as_view() ), name = 'org-client-account-credit-note-unallocated-list' ),



# ------ CLIENTS / ACCOUNT / REFUNDS ------------------

	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/refunds$', login_required( RefundList.as_view() ), name = 'org-client-account-refund-list' ),
	url( r'^(?P<oid>\d+)/client/(?P<cid>\d+)/account/refund/(?P<refid>\d+)$', login_required( RefundSingle.as_view() ), name = 'org-client-account-refund-single' ),


# ------ ACTIVITIES -----------------------------


	url( r'^(?P<oid>\d+)/activities$', login_required( ActivityList.as_view() ), name = 'org-activity-list' ),
	url( r'^(?P<oid>\d+)/activity/(?P<actid>\d+)$', login_required( ActivitySingle.as_view() ), name = 'org-activity-single' ),


	url( r'^(?P<oid>\d+)/activity/(?P<actid>\d+)/tasks$', login_required( TaskList.as_view() ), name = 'org-activity-task-list' ),
	url( r'^(?P<oid>\d+)/activity/(?P<actid>\d+)/task/(?P<taskid>\d+)$', login_required( TaskSingle.as_view() ), name = 'org-activity-task-single' ),


)


