from __future__ import unicode_literals

from django.db import models

import account.models as account_models

import uuid


AccountType = ChoicesEnum(
	ASSET = ( 10, 'Asset' ),
	LIABILITY = ( 10, 'Liability' ),
	EQUITY = ( 10, 'Equity' ),
	EXPENSE = ( 10, 'Expense' ),
	REVENUE = ( 10, 'Revenue' )
)



ObjectState = ChoicesEnum(
	ACTIVE = ( 0, 'Active' ),
	ARCHIVED = ( 10, 'Archived' )
)


class Chart( models.Model ):
	organization = models.OneToOneField( account_models.Organization )


class Account( models.Model ):
	chart = models.ForeignKey( Chart )
	refnum = models.CharField( primary_key = True, max_length = 32,  default = uuid.uuid4().get_hex() )

	code = models.BigIntegerField()

	name = models.CharField( min_length = 3, max_length = 256 )
	description = models.TextField( blank = True, default = '' )






