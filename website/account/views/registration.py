from django.views.generic import FormView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from ..models import *
from ..forms import *

from ..support import AccountSupport
from ..utils.email import send_templated_email

import datetime



class RegistrationStep1( FormView ):
	template_name = 'pages/account/register_step1.html'
	form_class = RegistrationForm
	success_url = 'register-step2'

	def form_valid( self, form ):
		rc = super( RegistrationStep1, self ).form_valid( form )

		cd = form.cleaned_data
		username = cd[ 'email_address' ]
		password = cd[ 'password1' ]
		firstname = cd[ 'first_name' ]
		lastname = cd[ 'last_name' ]

		luser = AccountSupport.create(
					username = username,
					password = password,
					firstname = firstname,
					lastname = lastname
				)

		send_templated_email( luser, 'authentication_request' )
		return rc


	def get_success_url( self ):
		return reverse( self.success_url )


class RegistrationStep2( FormView ):
	template_name = 'pages/account/register_step2.html'
	form_class = AuthenticationCodeForm
	success_url = 'login'

	def form_valid( self, form ):
		rc = super( RegistrationStep2, self ).form_valid( form )
		authcode = form.cleaned_data[ 'authcode' ]

		luser = User.objects.get( authenticationcode__authentication_code = authcode )
		profile = luser.get_profile()

		if profile.state != ProfileState.UNAUTHENTICATED:
			return rc

		AccountSupport.authenticate( luser )
		send_templated_email( luser, 'registration_successful' )
		return rc

	def get_success_url( self ):
		return reverse( self.success_url )



