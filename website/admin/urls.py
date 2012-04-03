from django.contrib.auth.decorators import login_required

from django.conf.urls import patterns, url

from views import *


urlpatterns = patterns('',

	url( r'^update$',
		login_required( UpdateView.as_view() ),
		name = 'admin-update'
	),

)


