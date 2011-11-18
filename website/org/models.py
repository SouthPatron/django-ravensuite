from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User

from utils.enum import ChoicesEnum

Interval = ChoicesEnum(
	MINUTE = ( 0, 'Minute' ),
	HOUR = ( 1, 'Hour' ),
	DAY = ( 2, 'Day' ),
	WEEK = ( 3, 'Week' ),
	MONTH = ( 4, 'Month' ),
	YEAR = ( 5, 'Year' ),
)

State = ChoicesEnum(
	DRAFT = ( 0, 'Draft' ),
	FINAL = ( 5, 'Final' ),
	VOID = ( 10, 'Void' ),
)

ExpiryAction = ChoicesEnum(
	COMMIT = ( 'commit', 'Commit' ),
	ROLLBACK = ( 'rollback', 'Rollback' ),
)






class DebugControl( models.Model ):
	current_time = models.DateTimeField()




class SystemCounter( models.Model ):
	account_no = models.BigIntegerField( default = 1 )
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
		

class OrganizationAccount( models.Model ):
	organization = models.OneToOneField( Organization )

class OrganizationCounter( models.Model ):
	organization = models.OneToOneField( Organization )
	invoice_no = models.BigIntegerField( default = 1 )
	client_no = models.BigIntegerField( default = 1 )
	tab_no = models.BigIntegerField( default = 1 )


"""
class UserRole( models.Model ):
	organization = models.ForeignKey( Organization )
	role = models.CharField( max_length = 192 )
	description = models.CharField( max_length = 192 )


class UserGroup( models.Model ):
	organization = models.ForeignKey( Organization )
	name = models.CharField( max_length = 192 )
	description = models.CharField( max_length = 192 )
	roles = models.ManyToManyField( UserRole )
	members = models.ManyToManyField( User )
"""


class Client( models.Model ):
	organization = models.ForeignKey( Organization )
	refnum = models.BigIntegerField()
	trading_name = models.CharField( max_length = 192 )

	def get_org( self ):
		return self.organization

	def get_single_url( self ):
		return reverse( 'org-client-single', kwargs = { 'oid' : self.organization.refnum, 'cid' : self.refnum } )
	
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
	total = models.BigIntegerField( default = 0 )
	is_paid = models.BooleanField( default = False )

	state = models.IntegerField( choices = State.choices(), default = State.DRAFT )


class InvoiceLine( models.Model ):
	invoice = models.ForeignKey( Invoice )
	event_time = models.DateTimeField()
	description = models.CharField( max_length = 64 )
	units = models.BigIntegerField( default = 0 )
	perunit = models.BigIntegerField( default = 0 )
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
	description = models.TextField()

	def get_org( self ):
		return self.organization

	def get_task_list_url( self ):
		return reverse( 'org-activity-task-list', kwargs = { 'oid' : self.get_org().refnum, 'actid' : self.id } )

	def get_single_url( self ):
		return reverse( 'org-activity-single', kwargs = { 'oid' : self.get_org().refnum, 'actid' : self.id } )


class Task( models.Model ):
	activity = models.ForeignKey( Activity )
	name = models.CharField( max_length = 32 )
	description = models.TextField()

	def get_org( self ):
		return self.activity.organization

	def get_activity( self ):
		return self.activity

	def get_single_url( self ):
		return reverse( 'org-activity-task-single', kwargs = { 'oid' : self.get_org().refnum, 'actid' : self.get_activity().id, 'taskid' : self.id } )



