from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required
from django.conf.urls import url, patterns

from views import *



urlpatterns = patterns('',

	url( r'^/dashboard$', login_required( Dashboard.as_view() ), name = 'contacts-dashboard' ),
	url( r'^/contacts$', login_required( ContactList.as_view() ), name = 'contacts-contact-list' ),
	url( r'^/groups$', login_required( GroupList.as_view() ), name = 'contacts-group-list' ),

)

