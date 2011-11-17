from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from utils.enum import ChoicesEnum

ProfileState = ChoicesEnum(
		UNAUTHENTICATED = ( 'unauthenticated', 'Unauthenticated' ),
		ACTIVE = ( 'active', 'Active' ),
		BLOCKED = ( 'blocked', 'Blocked' ),
		DISABLED = ( 'disabled', 'Disabled' ),
		DELETED = ( 'deleted', 'Deleted' ),
	)


class SystemCounter( models.Model ):
	profile_no = models.BigIntegerField( default = 1 )


class UserProfile( models.Model ):
	user = models.OneToOneField( User, unique=True )
	refnum = models.BigIntegerField()
	state = models.CharField( max_length = 16, choices = ProfileState.choices(), default = 'unauthenticated' )
	creation_time = models.DateTimeField()


class AuthenticationCode( models.Model ):
	user = models.OneToOneField( User, unique=True )
	creation_time = models.DateTimeField()
	authentication_code = models.CharField( blank=True, max_length=16, unique=True )


