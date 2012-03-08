from django.contrib.auth.decorators import login_required

from django.conf.urls.defaults import *

from views import *


urlpatterns = patterns('',

	url( r'^update$',
		login_required( UpdateView.as_view() ),
		name = 'admin-update'
	),

)


