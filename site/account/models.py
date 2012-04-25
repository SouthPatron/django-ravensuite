from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email

from common.utils.enum import ChoicesEnum

import uuid


ProfileState = ChoicesEnum(
		UNAUTHENTICATED = ( 'unauthenticated', 'Unauthenticated' ),
		ACTIVE = ( 'active', 'Active' ),
		BLOCKED = ( 'blocked', 'Blocked' ),
		DISABLED = ( 'disabled', 'Disabled' ),
		DELETED = ( 'deleted', 'Deleted' ),
	)

OrganizationState = ChoicesEnum(
	ACTIVE = ( 0, 'Active' ),
	ARCHIVED = ( 10, 'Archived' )
)


class UserProfile( models.Model ):
	user = models.OneToOneField( User, unique=True )
	state = models.CharField( max_length = 16, choices = ProfileState.choices(), default = ProfileState.UNAUTHENTICATED )
	creation_time = models.DateTimeField()
	last_seen = models.DateTimeField()

	def __unicode__( self ):
		return '{}'.format( self.user )


class AuthenticationCode( models.Model ):
	profile = models.OneToOneField( UserProfile )
	creation_time = models.DateTimeField()
	authentication_code = models.CharField( blank=True, max_length=16, unique=True )

	def __unicode__( self ):
		return '{} - {}'.format( self.user.email, self.authentication_code )



class Organization( models.Model ):
	refnum = models.CharField( primary_key = True, max_length = 32,  default = uuid.uuid4().get_hex() )
	profile = models.OneToOneField( UserProfile )

	state = models.IntegerField( choices = OrganizationState.choices(), default = OrganizationState.ACTIVE ) 

	trading_name = models.CharField( max_length = 192 )

	telephone_number = models.CharField( max_length = 64, blank = True, default = '' )
	fax_number = models.CharField( max_length = 64, blank = True, default = '' )
	email_address = models.CharField( max_length = 256, blank = True, default = '', validators=[validate_email] )
	postal_address = models.TextField( blank = True, default = '' )
	physical_address = models.TextField( blank = True, default = '' )

	def __unicode__( self ):
		return self.trading_name

	@models.permalink
	def get_absolute_url(self):
		return ('account-org-single', (), { 'oid' : self.refnum } )



