from django.conf.urls import patterns, url

from views.static import static_serve


urlpatterns = patterns('',

	url(r'^(?P<path_name>.*)',
		static_serve,
		name = 'static'
	)
)



