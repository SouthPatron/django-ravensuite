from django.views.generic import FormView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from ..utils.email import send_templated_email

from ..forms import *
from ..models import *

class ResendAuthCode( FormView ):
	template_name = 'pages/account/resend-authcode.html'
	form_class = EmailRequestForm
	success_url = 'register-step2'

	def get_success_url( self ):
		return reverse( self.success_url )

	def form_valid( self, form ):
		rc = super( ResendAuthCode, self ).form_valid( form )

		email_address = form.cleaned_data[ 'email_address' ]
		luser = User.objects.get( email = email_address )
		send_templated_email( luser, 'authentication_request' )
		return rc


class ResetPassword( FormView ):
	template_name = 'pages/account/password-reset.html'
	form_class = EmailRequestForm
	success_url = 'login'

	def get_success_url( self ):
		return reverse( self.success_url )

	def form_valid( self, form ):
		rc = super( ResetPassword, self ).form_valid( form )

		email_address = form.cleaned_data[ 'email_address' ]
		luser = User.objects.get( email = email_address )
		new_password = User.objects.make_random_password()
		luser.set_password( new_password )
		luser.save()
		send_templated_email( luser, 'password_reset', { 'new_password' : new_password } )
		return rc



