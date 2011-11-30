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
	CANCEL = ( 99, 'Cancel' ),
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
	account_no = models.BigIntegerField( default = 1 )
	tab_no = models.BigIntegerField( default = 1 )
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
	client_no = models.BigIntegerField( default = 1 )
	tab_no = models.BigIntegerField( default = 1 )
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
	
	def get_account_list_url( self ):
		return reverse( 'org-client-account-list', kwargs = { 'oid' : self.organization.refnum, 'cid' : self.refnum } )

	def get_tab_list_url( self ):
		return reverse( 'org-client-tab-list', kwargs = { 'oid' : self.organization.refnum, 'cid' : self.refnum } )
	
	

class Account( models.Model ):
	client = models.ForeignKey( Client )
	refnum = models.BigIntegerField( unique = True )

	transaction_no = models.BigIntegerField( default = 1 )

	is_enabled = models.BooleanField( default = True )
	name = models.CharField( max_length = 64 )
	min_balance = models.BigIntegerField( default = 0 )
	balance = models.BigIntegerField( default = 0 )

	def get_org( self ):
		return self.client.organization

	def get_client( self ):
		return self.client

	def get_single_url( self ):
		return reverse( 'org-client-account-single', kwargs = { 'oid' : self.client.organization.refnum, 'cid' : self.client.refnum, 'aid' : self.refnum } )
	
	def get_transaction_list_url( self ):
		return reverse( 'org-client-account-transaction-list', kwargs = { 'oid' : self.client.organization.refnum, 'cid' : self.client.refnum, 'aid' : self.refnum } )

	def get_invoice_list_url( self ):
		return reverse( 'org-client-account-invoice-list', kwargs = { 'oid' : self.client.organization.refnum, 'cid' : self.client.refnum, 'aid' : self.refnum } )


	

class AccountTransaction( models.Model ):
	account = models.ForeignKey( Account )
	refnum = models.BigIntegerField( default = 1 )
	event_time = models.DateTimeField()
	group = models.CharField( max_length = 32 )
	description = models.CharField( max_length = 64 )
	balance_before = models.BigIntegerField( default = 0 )
	balance_after = models.BigIntegerField( default = 0 )
	amount = models.BigIntegerField( default = 0 )

	def get_org( self ):
		return self.account.client.organization

	def get_client( self ):
		return self.account.client

	def get_account( self ):
		return self.account

	def get_single_url( self ):
		return reverse( 'org-client-account-transaction-single', kwargs = { 'oid' : self.get_org().refnum, 'cid' : self.get_client().refnum, 'aid' : self.get_account().refnum } )


class AccountTransactionData( models.Model ):
	account_transaction = models.OneToOneField( AccountTransaction )
	data = models.TextField()

class Tab( models.Model ):
	client = models.ForeignKey( Client )
	refnum = models.BigIntegerField( unique = True )

	transaction_no = models.BigIntegerField( default = 1 )

	is_enabled = models.BooleanField( default = True )
	name = models.CharField( max_length = 64 )
	min_balance = models.BigIntegerField( default = 0 )

	balance = models.BigIntegerField( default = 0 )
	reserved = models.BigIntegerField( default = 0 )

	def get_org( self ):
		return self.client.organization

	def get_client( self ):
		return self.client

	def get_single_url( self ):
		return reverse( 'org-client-tab-single', kwargs = { 'oid' : self.get_org().refnum, 'cid' : self.get_client().refnum, 'tabid' : self.refnum } )

	def get_transaction_list_url( self ):
		return reverse( 'org-client-tab-transaction-list', kwargs = { 'oid' : self.get_org().refnum, 'cid' : self.get_client().refnum, 'tabid' : self.refnum } )

	def get_reservation_list_url( self ):
		return reverse( 'org-client-tab-reservation-list', kwargs = { 'oid' : self.get_org().refnum, 'cid' : self.get_client().refnum, 'tabid' : self.refnum } )




class TabTransaction( models.Model ):
	tab = models.ForeignKey( Tab )
	refnum = models.BigIntegerField( default = 1 )
	event_time = models.DateTimeField()
	group = models.CharField( max_length = 32 )
	description = models.CharField( max_length = 64 )
	balance_before = models.BigIntegerField( default = 0 )
	balance_reserved = models.BigIntegerField( default = 0 )
	balance_after = models.BigIntegerField( default = 0 )
	amount = models.BigIntegerField( default = 0 )

	def get_org( self ):
		return self.tab.client.organization

	def get_client( self ):
		return self.tab.client

	def get_tab( self ):
		return self.tab

	def get_single_url( self ):
		return reverse( 'org-client-tab-transaction-single', kwargs = { 'oid' : self.get_org().refnum, 'cid' : self.get_client().refnum, 'tabid' : self.get_tab().refnum, 'tid' : self.refnum } )


class TabTransactionData( models.Model ):
	tab_transaction = models.OneToOneField( TabTransaction )
	data = models.TextField()


class Reservation( models.Model ):
	tab = models.ForeignKey( Tab )
	event_time = models.DateTimeField()
	expiry_time = models.DateTimeField()
	expiry_action = models.CharField( choices = ExpiryAction.choices(), default = ExpiryAction.COMMIT, max_length = 16 )
	group = models.CharField( max_length = 32 )
	description = models.CharField( max_length = 64 )
	uuid = models.CharField( max_length = 32, unique = True )
	amount = models.BigIntegerField()

	def get_org( self ):
		return self.tab.client.organization

	def get_client( self ):
		return self.tab.client

	def get_tab( self ):
		return self.tab

	def get_single_url( self ):
		return reverse( 'org-client-tab-reservation-single', kwargs = { 'oid' : self.get_org().refnum, 'cid' : self.get_client().refnum, 'tabid' : self.get_tab().refnum, 'rid' : self.uuid } )


class ReservationData( models.Model ):
	reservation = models.OneToOneField( Reservation )
	data = models.TextField()


class Invoice( models.Model ):
	account = models.ForeignKey( Account )
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
		return self.account.client.organization

	def get_client( self ):
		return self.account.client

	def get_account( self ):
		return self.account

	def get_single_url( self ):
		return reverse( 'org-client-account-invoice-single', kwargs = { 'oid' : self.get_org().refnum, 'cid' : self.get_client().refnum, 'aid' : self.get_account().refnum, 'iid' : self.refnum } )


class InvoiceLine( models.Model ):
	invoice = models.ForeignKey( Invoice )
	description = models.CharField( max_length = 64 )
	units = models.BigIntegerField( default = 0 )
	perunit = models.BigIntegerField( default = 0 )
	tax_rate = models.IntegerField( choices = TaxRate.choices() ) 
	total = models.BigIntegerField( default = 0 )

class Payment( models.Model ):
	invoice = models.ForeignKey( Invoice )
	transaction = models.ForeignKey( AccountTransaction )
	
	
class Subscription( models.Model ):
	account = models.ForeignKey( Account )

	interval_unit = models.IntegerField( choices = Interval.choices(), default = Interval.MONTH )
	interval_count = models.IntegerField( default = 1 )

	generate_invoice = models.BooleanField()
	generate_statement = models.BooleanField()

	group = models.CharField( max_length = 32 )
	is_grouped = models.BooleanField()
	description = models.CharField( max_length = 64 )

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






