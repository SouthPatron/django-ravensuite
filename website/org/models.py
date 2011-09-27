from __future__ import unicode_literals

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
)



class DebugControl( models.Model ):
	current_time = models.DateTimeField()

class Organization( models.Model ):
	trading_name = models.CharField( max_length = 192 )

class OrganizationAccount( models.Model ):
	organization = models.ForeignKey( Organization )

class Client( models.Model ):
	organization = models.ForeignKey( Organization )
	name = models.CharField( max_length = 192 )

class Account( models.Model ):
	client = models.ForeignKey( Client )
	is_enabled = models.BooleanField( default = True )
	name = models.CharField( max_length = 64 )

	min_balance = models.BigIntegerField( default = 0 )

	balance = models.BigIntegerField( default = 0 )
	reserved = models.BigIntegerField( default = 0 )

class Transaction( models.Model ):
	account = models.ForeignKey( Account )
	event_time = models.DateTimeField()
	group = models.CharField( max_length = 32 )
	description = models.CharField( max_length = 64 )
	amount_before = models.BigIntegerField( default = 0 )
	amount_adjustment = models.BigIntegerField( default = 0 )
	amount_after = models.BigIntegerField( default = 0 )

	is_grouped = models.BooleanField()
	is_voided = models.BooleanField()

class TransactionData( models.Model ):
	transaction = models.ForeignKey( Transaction )
	data = models.TextField()

class Invoice( models.Model ):
	account = models.ForeignKey( Account )
	reference = models.CharField( max_length = 64 )
	creation_time = models.DateTimeField()
	invoice_date = models.DateField()
	due_date = models.DateField()
	total = models.BigIntegerField( default = 0 )
	is_paid = models.BooleanField()

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
	transaction = models.ForeignKey( Transaction )

	
class Reservation( models.Model ):
	account = models.ForeignKey( Account )
	event_time = models.DateTimeField()
	expiry_time = models.DateTimeField()
	uuid = models.CharField( max_length = 32 )
	amount = models.BigIntegerField()
	
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




