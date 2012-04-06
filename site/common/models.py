from __future__ import unicode_literals


from django.db import models
from django.db.models import F,Q
from django.contrib.auth.models import User
from django.core.validators import validate_email, MinLengthValidator

from common.utils.enum import ChoicesEnum

import uuid


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
	state = models.CharField( max_length = 16, choices = ProfileState.choices(), default = 'unauthenticated' )
	creation_time = models.DateTimeField()
	last_seen = models.DateTimeField()

	def __unicode__( self ):
		return '{}'.format( self.user )


class AuthenticationCode( models.Model ):
	user = models.OneToOneField( User, unique=True )
	creation_time = models.DateTimeField()
	authentication_code = models.CharField( blank=True, max_length=16, unique=True )

	def __unicode__( self ):
		return '{} - {}'.format( self.user.email, self.authentication_code )




# --- ORG ----------------------------------------------------


Interval = ChoicesEnum(
	MINUTE = ( 0, 'Minute' ),
	HOUR = ( 1, 'Hour' ),
	DAY = ( 2, 'Day' ),
	WEEK = ( 3, 'Week' ),
	MONTH = ( 4, 'Month' ),
	YEAR = ( 5, 'Year' ),
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

SourceDocumentType = ChoicesEnum(
	INVOICE = ( 0, 'Invoice' ),
	CREDIT_NOTE = ( 10, 'Credit Note' ),
	REFUND = ( 20, 'Refund' ),
	PAYMENT = ( 30, 'Payment' )
)

SourceDocumentState = ChoicesEnum(
	DRAFT = ( 0, 'Draft' ),
	FINAL = ( 10, 'Final' ),
	VOID = ( 20, 'Void' ),
	DELETE = ( 99, 'Delete' ),
)

ObjectState = ChoicesEnum(
	ACTIVE = ( 0, 'Active' ),
	ARCHIVED = ( 10, 'Archived' )
)



class Organization( models.Model ):
	state = models.IntegerField( choices = ObjectState.choices() ) 

	trading_name = models.CharField( max_length = 192 )
	refnum = models.CharField( max_length = 32, unique = True, default = uuid.uuid4().get_hex() )

	telephone_number = models.CharField( max_length = 64, blank = True, default = '' )
	fax_number = models.CharField( max_length = 64, blank = True, default = '' )
	email_address = models.CharField( max_length = 256, blank = True, default = '', validators=[validate_email] )
	postal_address = models.TextField( blank = True, default = '' )
	physical_address = models.TextField( blank = True, default = '' )

	def __unicode__( self ):
		return self.trading_name

	@models.permalink
	def get_absolute_url(self):
		return ('org-single', (), { 'oid' : self.refnum } )
	
	@models.permalink
	def get_client_list_url( self ):
		return ( 'org-client-list', (), { 'oid' : self.refnum } )

	@models.permalink
	def get_activity_list_url( self ):
		return ( 'org-activity-list', (), { 'oid' : self.refnum } )

	@models.permalink
	def get_user_list_url( self ):
		return ( 'org-admin-user-list', (), { 'oid' : self.refnum } )

	def get_org( self ):
		return self


class OrganizationSettings( models.Model ):
	class Meta:
		verbose_name_plural = 'Organization Settings'

	organization = models.OneToOneField( Organization )

	def get_org( self ):
		return self.organization

	def __unicode__( self ):
		return self.organization.trading_name


class OrganizationAccount( models.Model ):
	organization = models.OneToOneField( Organization )

	def __unicode__( self ):
		return self.organization.trading_name


class OrganizationCounter( models.Model ):
	organization = models.OneToOneField( Organization )

	source_document_no =  models.BigIntegerField( default = 1 )

	client_no = models.BigIntegerField( default = 1 )
	project_no = models.BigIntegerField( default = 1 )

	def __unicode__( self ):
		return self.organization.trading_name




class UserMembership( models.Model ):
	user = models.ForeignKey( User )
	organization = models.ForeignKey( Organization )
	category = models.IntegerField( choices = UserCategory.choices() ) 
	is_enabled = models.BooleanField( default = True )

	def get_org( self ):
		return self.organization
	
	def get_usermembership( self ):
		return self

	@models.permalink
	def get_absolute_url( self ):
		return ( 'org-admin-user-single', (), { 'oid' : self.organization.refnum, 'uid' : self.id } )

	def __unicode__( self ):
		return UserCategory.get( self.category )[1]


class UserPermission( models.Model ):
	user_membership = models.ForeignKey( UserMembership )
	entity = models.CharField( max_length = 255 )
	refnum = models.BigIntegerField()
	crud = models.CommaSeparatedIntegerField( max_length = 255, choices = CrudAccess.choices() )


class Client( models.Model ):
	state = models.IntegerField( choices = ObjectState.choices() ) 

	organization = models.ForeignKey( Organization )
	refnum = models.BigIntegerField()
	trading_name = models.CharField( max_length = 192, validators = [MinLengthValidator(1)] )

	telephone_number = models.CharField( max_length = 64, blank = True, default = '' )
	fax_number = models.CharField( max_length = 64, blank = True, default = '' )
	email_address = models.CharField( max_length = 256, blank = True, default = '', validators=[validate_email] )
	postal_address = models.TextField( blank = True, default = '' )
	physical_address = models.TextField( blank = True, default = '' )

	def __unicode__( self ):
		return self.trading_name

	def get_org( self ):
		return self.organization
	
	def get_client( self ):
		return self

	@models.permalink
	def get_absolute_url( self ):
		return ( 'org-client-single', (), { 'oid' : self.organization.refnum, 'cid' : self.refnum } )

	@models.permalink
	def get_project_list_url( self ):
		return ( 'org-client-project-list', (), { 'oid' : self.organization.refnum, 'cid' : self.refnum } )

	@models.permalink
	def get_account_single_url( self ):
		return ( 'org-client-account-single', (), { 'oid' : self.organization.refnum, 'cid' : self.refnum } )

	def get_account( self ):
		return Account.objects.get( client = self )



	# General Information -

	def get_available_funds_list( self ):
		return SourceDocument.objects.filter(
				Q( document_type = SourceDocumentType.PAYMENT ) |
				Q( document_type = SourceDocumentType.CREDIT_NOTE ),
				client = self,
				document_state = SourceDocumentState.FINAL,
				total__gt = F( 'allocated' )
			)



	# Transactions --------

	# Invoices ------------

	@models.permalink
	def get_invoice_list_url( self ):
		return ( 'org-client-account-transaction-invoice-list', (), { 'oid' : self.organization.refnum, 'cid' : self.refnum } )

	@models.permalink
	def get_draft_invoice_list_url( self ):
		return ( 'org-client-account-transaction-invoice-draft-list', (), { 'oid' : self.organization.refnum, 'cid' : self.refnum } )

	@models.permalink
	def get_unpaid_invoice_list_url( self ):
		return ( 'org-client-account-transaction-invoice-unpaid-list', (), { 'oid' : self.organization.refnum, 'cid' : self.refnum } )

	def get_unpaid_invoice_list( self ):
		return SourceDocument.objects.filter( client = self, document_type = SourceDocumentType.INVOICE, document_state = SourceDocumentState.FINAL, total__gt = F( 'allocated' ) )

	def get_unpaid_invoice_count( self ):
		return self.get_unpaid_invoice_list().count()



	# Credit Notes --------

	@models.permalink
	def get_draft_credit_note_list_url( self ):
		return ( 'org-client-account-transaction-credit-note-draft-list', (), { 'oid' : self.organization.refnum, 'cid' : self.refnum } )

	@models.permalink
	def get_unallocated_credit_note_list_url( self ):
		return ( 'org-client-account-transaction-credit-note-unallocated-list', (), { 'oid' : self.organization.refnum, 'cid' : self.refnum } )

	def get_unallocated_credit_note_count( self ):
		return SourceDocument.objects.filter( client = self, document_type = SourceDocumentType.CREDIT_NOTE, document_state = SourceDocumentState.FINAL, total__gt = F( 'allocated' ) ).count()


	# Payments ------------

	@models.permalink
	def get_unallocated_payment_list_url( self ):
		return ( 'org-client-account-transaction-payment-unallocated-list', (), { 'oid' : self.organization.refnum, 'cid' : self.refnum } )

	@models.permalink
	def get_draft_payment_list_url( self ):
		return ( 'org-client-account-transaction-payment-draft-list', (), { 'oid' : self.organization.refnum, 'cid' : self.refnum } )

	def get_draft_payment_count( self ):
		return SourceDocument.objects.filter( client = self, document_type = SourceDocumentType.PAYMENT, document_state = SourceDocumentState.DRAFT ).count()

	def get_unallocated_payment_count( self ):
		return SourceDocument.objects.filter( client = self, document_type = SourceDocumentType.PAYMENT, document_state = SourceDocumentState.FINAL, total__gt = F( 'allocated' ) ).count()



	# Refunds -------------


	@models.permalink
	def get_refund_list_url( self ):
		return ( 'org-client-account-transaction-refund-list', (), { 'oid' : self.organization.refnum, 'cid' : self.refnum } )

	@models.permalink
	def get_unallocated_refund_list_url( self ):
		return ( 'org-client-account-transaction-refund-unallocated-list', (), { 'oid' : self.organization.refnum, 'cid' : self.refnum } )

	def get_unallocated_refund_count( self ):
		return SourceDocument.objects.filter( client = self, document_type = SourceDocumentType.REFUND, document_state = SourceDocumentState.FINAL, total__gt = F( 'allocated' ) ).count()




class SourceDocument( models.Model ):
	client = models.ForeignKey( Client )
	refnum = models.BigIntegerField()
	creation_time = models.DateTimeField()
	event_time = models.DateTimeField()

	document_type = models.IntegerField( choices = SourceDocumentType.choices() )
	document_state = models.IntegerField( choices = SourceDocumentState.choices() )

	amount = models.BigIntegerField( default = 0 )
	tax = models.BigIntegerField( default = 0 )
	total = models.BigIntegerField( default = 0 )


	allocated = models.BigIntegerField( default = 0 )


	def __unicode__( self ):
		return '{} {}'.format(
			SourceDocumentType.get( self.document_type )[1],
			self.refnum
			)


	def get_org( self ):
		return self.client.organization

	def get_client( self ):
		return self.client

	def get_account( self ):
		return self.get_client().account


	@models.permalink
	def get_absolute_url( self ):
		my_route = None

		if self.document_type == SourceDocumentType.INVOICE:
			my_route = 'org-client-account-transaction-invoice-single'

		if self.document_type == SourceDocumentType.PAYMENT:
			my_route = 'org-client-account-transaction-payment-single'

		if self.document_type == SourceDocumentType.CREDIT_NOTE:
			my_route = 'org-client-account-transaction-credit-note-single'

		if self.document_type == SourceDocumentType.REFUND:
			my_route = 'org-client-account-transaction-refund-single'

		return ( my_route, (), { 'oid' : self.get_org().refnum, 'cid' : self.get_client().refnum, 'sdid' : self.refnum } )


	class Meta:
		ordering = [ '-event_time' ]


class SourceDocumentMeta( models.Model ):
	source_document = models.ForeignKey( SourceDocument )
	key = models.CharField( max_length = 255 )
	value = models.CharField( max_length = 255 )
	
class SourceDocumentLine( models.Model ):
	source_document = models.ForeignKey( SourceDocument )

	description = models.CharField( max_length = 64 )
	units = models.BigIntegerField( default = 0 )
	perunit = models.BigIntegerField( default = 0 )
	amount = models.BigIntegerField( default = 0 )
	tax_rate = models.IntegerField( choices = TaxRate.choices() ) 
	tax_amount = models.BigIntegerField( default = 0 )
	total = models.BigIntegerField( default = 0 )


class SourceDocumentAllocation( models.Model ):
	source = models.ForeignKey( SourceDocument, related_name = 'source_allocation' )
	destination = models.ForeignKey( SourceDocument, related_name = 'destination_allocation' )
	amount = models.BigIntegerField( default = 0 )



class Account( models.Model ):
	client = models.OneToOneField( Client )
	transaction_no = models.BigIntegerField( default = 1 )
	balance = models.BigIntegerField( default = 0 )

	def get_org( self ):
		return self.client.organization

	def get_client( self ):
		return self.client

	def get_account( self ):
		return self

	@models.permalink
	def get_absolute_url( self ):
		return ( 'org-client-account-single', (), { 'oid' : self.client.organization.refnum, 'cid' : self.client.refnum } )
	
	@models.permalink
	def get_transaction_list_url( self ):
		return ( 'org-client-account-transaction-list', (), { 'oid' : self.client.organization.refnum, 'cid' : self.client.refnum } )

	def __unicode__( self ):
		return self.client.__unicode__()


class AccountTransaction( models.Model ):
	account = models.ForeignKey( Account )
	refnum = models.BigIntegerField( default = 1 )
	creation_time = models.DateTimeField()
	event_time = models.DateTimeField()
	group = models.CharField( max_length = 32 )
	description = models.CharField( max_length = 64 )
	balance_before = models.BigIntegerField( default = 0 )
	balance_after = models.BigIntegerField( default = 0 )
	amount = models.BigIntegerField( default = 0 )

	source_document = models.ForeignKey( SourceDocument )


	def get_org( self ):
		return self.account.client.organization

	def get_client( self ):
		return self.account.client

	def get_account( self ):
		return self.account

	@models.permalink
	def get_absolute_url( self ):
		return ( 'org-client-account-transaction-single', (), { 'oid' : self.get_org().refnum, 'cid' : self.get_client().refnum, 'tid' : self.refnum } )

	class Meta:
		ordering = [ '-event_time', '-creation_time' ]


class AccountTransactionData( models.Model ):
	account_transaction = models.OneToOneField( AccountTransaction )
	data = models.TextField()





class Activity( models.Model ):
	class Meta:
		verbose_name_plural = 'Activities'

	organization = models.ForeignKey( Organization )
	name = models.CharField( max_length = 32 )
	description = models.TextField( blank = True )

	def __unicode__( self ):
		return self.name

	def get_org( self ):
		return self.organization
	
	def get_activity( self ):
		return self

	@models.permalink
	def get_task_list_url( self ):
		return ( 'org-activity-task-list', (), { 'oid' : self.get_org().refnum, 'actid' : self.id } )

	@models.permalink
	def get_absolute_url( self ):
		return ( 'org-activity-single', (), { 'oid' : self.get_org().refnum, 'actid' : self.id } )


class Task( models.Model ):
	activity = models.ForeignKey( Activity )
	name = models.CharField( max_length = 32 )
	description = models.TextField( blank = True )

	def __unicode__( self ):
		return self.name

	def get_org( self ):
		return self.activity.organization

	def get_activity( self ):
		return self.activity
	
	def get_task( self ):
		return self

	@models.permalink
	def get_absolute_url( self ):
		return ( 'org-activity-task-single', (), { 'oid' : self.get_org().refnum, 'actid' : self.get_activity().id, 'taskid' : self.id } )



class Project( models.Model ):
	client = models.ForeignKey( Client )
	refnum = models.BigIntegerField()

	status = models.IntegerField( choices = ProjectStatus.choices(), default = ProjectStatus.INACTIVE )

	name = models.CharField( max_length = 32 )
	description = models.TextField( blank = True )

	def __unicode__( self ):
		return self.name


	def get_org( self ):
		return self.client.organization

	def get_client( self ):
		return self.client

	def get_project( self ):
		return self

	@models.permalink
	def get_absolute_url( self ):
		return ( 'org-client-project-single', (), { 'oid' : self.get_org().refnum, 'cid' : self.get_client().refnum, 'pid' : self.refnum } )




# --- TIMESHEET --------------------------------------------------


class TimesheetEntry( models.Model ):
	class Meta:
		verbose_name_plural = 'Timesheet Entries'
		ordering = [ '-start_time' ]

	user = models.ForeignKey( User )
	project = models.ForeignKey( Project )
	task = models.ForeignKey( Task )
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

	@models.permalink
	def get_absolute_url( self ):
		return ( 'timesheet-timer-single', (), { 'timerid' : self.id } )


	class Meta:
		ordering = [ '-start_time' ]


