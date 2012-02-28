from django.conf.urls.defaults import *

from views.static import static_serve


urlpatterns = patterns('',

	url(r'^(?P<path_name>.*)',
		static_serve,
		name = 'static'
	)
)



