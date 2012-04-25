from django.utils.translation import ugettext as _

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, UpdateView

from ..forms import *


class ProfileView( DetailView ):
	template_name = 'pages/account/profile_view.html'

	def get_object( self ):
		return self.request.user


class ProfileEdit( UpdateView ):
	form_class = EditProfileForm
	template_name = 'pages/account/profile_edit.html'
	success_url = 'account-profile'

	def get_object( self ):
		return self.request.user

	def get_success_url( self ):
		return reverse( self.success_url )


class ProfileChangePassword( UpdateView ):
	form_class = ChangePasswordForm
	template_name = 'pages/account/profile_change_password.html'
	success_url = 'account-profile'

	def get_object( self ):
		return self.request.user

	def get_success_url( self ):
		return reverse( self.success_url )

	def form_valid( self, form ):
		messages.success( self.request, _('VMG_10001') )
		return super( ProfileChangePassword, self ).form_valid( form )

