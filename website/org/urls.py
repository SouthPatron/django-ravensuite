from django.conf.urls.defaults import *
from django.views.generic import RedirectView, UpdateView

from views import *
from models import *

urlpatterns = patterns('org.views',

	url( r'^$', 'index', name = 'org-index' ),

	url(
		r'^(?P<pk>\d+)$',
		Org.as_view(),
		{ 
		},
		name = 'org-org',
	),

)

