from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

from common.utils.enum import ChoicesEnum


# --- DEBUG -----------------------------------------------------


class DebugControl( models.Model ):
	current_time = models.DateTimeField()


# --- ACCOUNT ---------------------------------------------------

ProfileState = ChoicesEnum(
		UNAUTHENTICATED = ( 'unauthenticated', 'Unauthenticated' ),
		ACTIVE = ( 'active', 'Active' ),
		BLOCKED = ( 'blocked', 'Blocked' ),
		DISABLED = ( 'disabled', 'Disabled' ),
		DELETED = ( 'deleted', 'Deleted' ),
	)


class UserProfile( models.Model ):
	user = models.OneToOneField( User, unique=True )
	refnum = models.BigIntegerField()
	state = models.CharField( max_length = 16, choices = ProfileState.choices(), default = 'unauthenticated' )
	creation_time = models.DateTimeField()
	last_seen = models.DateTimeField()


class AuthenticationCode( models.Model ):
	user = models.OneToOneField( User, unique=True )
	creation_time = models.DateTimeField()
	authentication_code = models.CharField( blank=True, max_length=16, unique=True )




# --- ORG ----------------------------------------------------


Interval = ChoicesEnum(
	MINUTE = ( 0, 'Minute' ),
	HOUR = ( 1, 'Hour' ),
	DAY = ( 2, 'Day' ),
	WEEK = ( 3, 'Week' ),
	MONTH = ( 4, 'Month' ),
	YEAR = ( 5, 'Year' ),
)

InvoiceState = ChoicesEnum(
	DRAFT = ( 0, 'Draft' ),
	FINAL = ( 5, 'Final' ),
	VOID = ( 10, 'Void' ),
	DELETE = ( 99, 'Delete' ),
)

PaymentState = ChoicesEnum(
	ACTIVE = ( 5, 'Active' ),
	VOID = ( 10, 'Reversed' ),
)


ExpiryAction = ChoicesEnum(
	COMMIT = ( 'commit', 'Commit' ),
	ROLLBACK = ( 'rollback', 'Rollback' ),
)

UserCategory = ChoicesEnum(
	OWNER = ( 0, 'Owner' ),
	ADMINISTRATOR = ( 10, 'Administrator' ),
	EMPLOYEE = ( 20, 'Employee' ),
	CONTRACTOR = ( 30, 'Contractor' ),
	CLIENT = ( 40, 'Client' ),
	GUEST = ( 50, 'Guest' ),
)

CrudAccess = ChoicesEnum(
	CREATE = ( 0, 'Create' ),
	READ = ( 10, 'Read' ),
	UPDATE = ( 20, 'Update' ),
	DELETE = ( 30, 'Delete' ),
)

ProjectStatus = ChoicesEnum(
	INACTIVE = ( 0, 'Inactive' ),
	ACTIVE = ( 10, 'Active' ),
	COMPLETE = ( 20, 'Complete' ),
	MAINTENANCE = ( 30, 'Maintenance' ),
)


TaxRate = ChoicesEnum(
	NONE = ( 0, 'No Tax' ),
	INCLUSIVE = ( 1, 'Tax Inclusive' ),
	EXCLUSIVE = ( 2, 'Tax Exclusive' ),
	EXEMPT = ( 3, 'Tax Exempt' ),
)




class SystemCounter( models.Model ):
	profile_no = models.BigIntegerField( default = 1 )
	organization_no = models.BigIntegerField( default = 1 )

class Organization( models.Model ):
	trading_name = models.CharField( max_length = 192 )
	refnum = models.BigIntegerField( unique = True )

	def get_single_url( self ):
		return reverse( 'org-single', kwargs = { 'oid' : self.refnum } )
	
	def get_client_list_url( self ):
		return reverse( 'org-client-list', kwargs = { 'oid' : self.refnum } )

	def get_activity_list_url( self ):
		return reverse( 'org-activity-list', kwargs = { 'oid' : self.refnum } )

	def get_user_list_url( self ):
		return reverse( 'org-user-list', kwargs = { 'oid' : self.refnum } )
		

class OrganizationAccount( models.Model ):
	organization = models.OneToOneField( Organization )

class OrganizationCounter( models.Model ):
	organization = models.OneToOneField( Organization )
	invoice_no = models.BigIntegerField( default = 1 )
	payment_no = models.BigIntegerField( default = 1 )
	client_no = models.BigIntegerField( default = 1 )
	project_no = models.BigIntegerField( default = 1 )


class UserMembership( models.Model ):
	user = models.ForeignKey( User )
	organization = models.ForeignKey( Organization )
	category = models.IntegerField( choices = UserCategory.choices() ) 
	is_enabled = models.BooleanField( default = True )

	def get_org( self ):
		return self.organization

	def get_single_url( self ):
		return reverse( 'org-user-single', kwargs = { 'oid' : self.organization.refnum, 'uid' : self.id } )


class UserPermissions( models.Model ):
	user_membership = models.ForeignKey( UserMembership )
	entity = models.CharField( max_length = 255 )
	refnum = models.BigIntegerField()
	crud = models.CommaSeparatedIntegerField( max_length = 255, choices = CrudAccess.choices() )


class Client( models.Model ):
	organization = models.ForeignKey( Organization )
	refnum = models.BigIntegerField()
	trading_name = models.CharField( max_length = 192 )

	def get_org( self ):
		return self.organization

	def get_single_url( self ):
		return reverse( 'org-client-single', kwargs = { 'oid' : self.organization.refnum, 'cid' : self.refnum } )

	def get_project_list_url( self ):
		return reverse( 'org-client-project-list', kwargs = { 'oid' : self.organization.refnum, 'cid' : self.refnum } )
	
	def get_account_single_url( self ):
		return reverse( 'org-client-account-single', kwargs = { 'oid' : self.organization.refnum, 'cid' : self.refnum } )

	def get_invoice_list_url( self ):
		return reverse( 'org-client-account-invoice-list', kwargs = { 'oid' : self.organization.refnum, 'cid' : self.refnum } )

	def get_unpaid_invoice_list( self ):
		return Invoice.objects.filter( client = self, is_paid = False, state = InvoiceState.FINAL )

	def get_draft_invoice_list( self ):
		return Invoice.objects.filter( client = self, state = InvoiceState.DRAFT )

	def get_draft_invoice_list_url( self ):
		return reverse( 'org-client-account-invoice-draft-list', kwargs = { 'oid' : self.organization.refnum, 'cid' : self.refnum } )

	def get_unallocated_payments( self ):
		return Payment.objects.filter( client = self, is_allocated = False, state = PaymentState.ACTIVE )

	def get_unallocated_payment_amount( self ):
		total_amount = 0
		for pmt in Payment.objects.filter( client = self, is_allocated = False, state = PaymentState.ACTIVE ):
			total_amount += pmt.get_amount_free()
		return total_amount




class Account( models.Model ):
	client = models.OneToOneField( Client )
	transaction_no = models.BigIntegerField( default = 1 )
	balance = models.BigIntegerField( default = 0 )

	def get_org( self ):
		return self.client.organization

	def get_client( self ):
		return self.client

	def get_single_url( self ):
		return reverse( 'org-client-account-single', kwargs = { 'oid' : self.client.organization.refnum, 'cid' : self.client.refnum } )
	
	def get_transaction_list_url( self ):
		return reverse( 'org-client-account-transaction-list', kwargs = { 'oid' : self.client.organization.refnum, 'cid' : self.client.refnum } )


class AccountTransaction( models.Model ):
	account = models.ForeignKey( Account )
	refnum = models.BigIntegerField( default = 1 )
	event_time = models.DateTimeField()
	group = models.CharField( max_length = 32 )
	description = models.CharField( max_length = 64 )
	balance_before = models.BigIntegerField( default = 0 )
	balance_after = models.BigIntegerField( default = 0 )
	amount = models.BigIntegerField( default = 0 )

	originating_route = models.CharField( max_length = 255 )


	def get_org( self ):
		return self.account.client.organization

	def get_client( self ):
		return self.account.client

	def get_account( self ):
		return self.account

	def get_single_url( self ):
		return reverse( 'org-client-account-transaction-single', kwargs = { 'oid' : self.get_org().refnum, 'cid' : self.get_client().refnum, 'tid' : self.refnum } )

	class Meta:
		ordering = [ '-event_time' ]


class AccountTransactionData( models.Model ):
	account_transaction = models.OneToOneField( AccountTransaction )
	data = models.TextField()


class Invoice( models.Model ):
	client = models.ForeignKey( Client )
	refnum = models.BigIntegerField()
	creation_time = models.DateTimeField()
	invoice_date = models.DateField()
	due_date = models.DateField()
	amount = models.BigIntegerField( default = 0 )
	tax = models.BigIntegerField( default = 0 )
	total = models.BigIntegerField( default = 0 )

	comment = models.CharField( max_length = 255 )

	is_paid = models.BooleanField( default = False )

	state = models.IntegerField( choices = InvoiceState.choices(), default = InvoiceState.DRAFT )

	def get_org( self ):
		return self.client.organization

	def get_client( self ):
		return self.client

	def get_single_url( self ):
		return reverse( 'org-client-account-invoice-single', kwargs = { 'oid' : self.get_org().refnum, 'cid' : self.get_client().refnum, 'iid' : self.refnum } )

	def get_amount_outstanding( self ):
		return ( self.total - self.get_amount_paid() )

	def get_amount_paid( self ):
		q = PaymentAllocation.objects.filter( invoice = self ).aggregate( allocated = models.Sum( 'amount' ) )
		allocated = q[ 'allocated' ]
		if allocated is None:
			return 0
		return allocated


	def is_draft( self ):
		return self.state == InvoiceState.DRAFT

	def is_final( self ):
		return self.state == InvoiceState.FINAL

	def is_void( self ):
		return self.state == InvoiceState.VOID

	class Meta:
		ordering = [ '-invoice_date' ]


class InvoiceLine( models.Model ):
	invoice = models.ForeignKey( Invoice )
	description = models.CharField( max_length = 64 )
	units = models.BigIntegerField( default = 0 )
	perunit = models.BigIntegerField( default = 0 )
	tax_rate = models.IntegerField( choices = TaxRate.choices() ) 
	total = models.BigIntegerField( default = 0 )

class Payment( models.Model ):
	client = models.ForeignKey( Client )
	refnum = models.BigIntegerField()
	creation_time = models.DateTimeField()
	payment_date = models.DateField()
	amount = models.BigIntegerField( default = 0 )

	comment = models.CharField( max_length = 255 )

	is_allocated = models.BooleanField( default = False )

	state = models.IntegerField( choices = PaymentState.choices(), default = PaymentState.ACTIVE )

	def get_org( self ):
		return self.client.organization

	def get_client( self ):
		return self.client

	def get_single_url( self ):
		return reverse( 'org-client-account-payment-single', kwargs = { 'oid' : self.get_org().refnum, 'cid' : self.get_client().refnum, 'payid' : self.refnum } )
	def get_amount_free( self ):
		return ( self.amount - self.get_amount_allocated() )

	def get_amount_allocated( self ):
		q = PaymentAllocation.objects.filter( payment = self ).aggregate( allocated = models.Sum( 'amount' ) )
		allocated = q['allocated']
		if allocated is None:
			return 0
		return allocated

	class Meta:
		ordering = [ '-payment_date' ]

class PaymentAllocation( models.Model ):
	payment = models.ForeignKey( Payment )
	invoice = models.ForeignKey( Invoice )
	amount = models.BigIntegerField( default = 0 )




class Activity( models.Model ):
	organization = models.ForeignKey( Organization )
	name = models.CharField( max_length = 32 )
	description = models.TextField( blank = True )

	def get_org( self ):
		return self.organization

	def get_task_list_url( self ):
		return reverse( 'org-activity-task-list', kwargs = { 'oid' : self.get_org().refnum, 'actid' : self.id } )

	def get_single_url( self ):
		return reverse( 'org-activity-single', kwargs = { 'oid' : self.get_org().refnum, 'actid' : self.id } )


class Task( models.Model ):
	activity = models.ForeignKey( Activity )
	name = models.CharField( max_length = 32 )
	description = models.TextField( blank = True )

	def get_org( self ):
		return self.activity.organization

	def get_activity( self ):
		return self.activity

	def get_single_url( self ):
		return reverse( 'org-activity-task-single', kwargs = { 'oid' : self.get_org().refnum, 'actid' : self.get_activity().id, 'taskid' : self.id } )



class Project( models.Model ):
	client = models.ForeignKey( Client )
	refnum = models.BigIntegerField()

	status = models.IntegerField( choices = ProjectStatus.choices(), default = ProjectStatus.INACTIVE )

	name = models.CharField( max_length = 32 )
	description = models.TextField( blank = True )

	def get_org( self ):
		return self.client.organization

	def get_client( self ):
		return self.client

	def get_single_url( self ):
		return reverse( 'org-client-project-single', kwargs = { 'oid' : self.get_org().refnum, 'cid' : self.get_client().refnum, 'pid' : self.refnum } )




# --- TIMESHEET --------------------------------------------------


class TimesheetEntry( models.Model ):
	user = models.ForeignKey( User )
	project = models.ForeignKey( Project )
	task = models.ForeignKey( Task )
	invoice = models.ForeignKey( Invoice, null = True, default = None )
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	description = models.CharField( max_length = 255, blank = True )

	def get_org( self ):
		return self.project.client.organization

	def get_client( self ):
		return self.project.client

	def get_activity( self ):
		return self.task.activity


	class Meta:
		ordering = [ '-start_time' ]


class TimesheetTimer( models.Model ):
	user = models.ForeignKey( User )
	project = models.ForeignKey( Project )
	task = models.ForeignKey( Task )
	start_time = models.DateTimeField()
	description = models.CharField( max_length = 255, blank = True )

	def get_org( self ):
		return self.project.client.organization

	def get_client( self ):
		return self.project.client

	def get_activity( self ):
		return self.task.activity

	def get_single_url( self ):
		return reverse( 'timesheet-timer-single', kwargs = { 'timerid' : self.id } )


	class Meta:
		ordering = [ '-start_time' ]


