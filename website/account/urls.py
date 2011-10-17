from django.conf.urls.defaults import *
from django.views.generic import RedirectView

from views import *

urlpatterns = patterns('',
	url( r'^login$', LoginView.as_view(), name='login' ),
	url( r'^logout$', logout_view, name='logout' ),

	url(
		r'^register$',
		RedirectView.as_view( url='register/step1' ),
		name='register-url'
	),

	url( r'^register/step1$', RegistrationStep1.as_view(), name='register-step1'),

	url( r'^register/step2$', RegistrationStep2.as_view(), name='register-step2'),

	url( r'^resend-authentication-code$', ResendAuthCode.as_view(), name='resend-authentication-code'),

	url( r'^password-reset$', ResetPassword.as_view(), name='password-reset'),



	url( r'^members/account/profile$', RedirectView.as_view( url='profile/view'), name = 'account-profile' ),
	url( r'^members/account/profile/view$', ProfileView.as_view(), name = 'account-profile-view' ),
	url( r'^members/account/profile/edit$', ProfileEdit.as_view(), name = 'account-profile-edit' ),
	url( r'^members/account/profile/change-password$', ProfileChangePassword.as_view(), name = 'account-profile-change-password' ),



)



