from django.views.generic import FormView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from common.buslog.account import *

from ..forms import *


class LoginView( FormView ):
	template_name = 'pages/account/login.html'
	form_class = LoginForm
	success_url = 'account-profile'

	def form_valid( self, form ):
		rc = super( LoginView, self ).form_valid( form )

		cd = form.cleaned_data

		AuthBusLog.login(
					self.request,
					username = cd['email_address'],
					password = cd['password'],
				)

		if self.request.GET.get( 'next', None ) is not None:
			return redirect( self.request.GET[ 'next' ] )

		return rc

	def get_success_url( self ):
		return reverse( self.success_url )


def logout_view( request ):
	AuthBusLog.logout( request )
	return redirect( 'home-index' )


