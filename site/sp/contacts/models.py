from __future__ import unicode_literals

from django.db import models
from django.core.validators import validate_email



import account.models as account_models


class ContactLink( models.Model ):
	organization = models.OneToOneField( account_models.Organization )


class Group( models.Model ):
	link = models.ForeignKey( ContactLink )

	name = models.CharField( max_length = 256 )


class Contact( models.Model ):
	link = models.ForeignKey( ContactLink )
	group = models.ManyToManyField( Group )

	trading_name = models.CharField( max_length = 256 )

	telephone_number = models.CharField( max_length = 64, blank = True, default = '' )
	fax_number = models.CharField( max_length = 64, blank = True, default = '' )
	email_address = models.CharField( max_length = 256, blank = True, default = '', validators=[validate_email] )
	postal_address = models.TextField( blank = True, default = '' )
	physical_address = models.TextField( blank = True, default = '' )





