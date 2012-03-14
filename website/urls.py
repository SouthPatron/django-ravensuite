from django.conf.urls.defaults import patterns, include, url
from django.views.generic import RedirectView


urlpatterns = patterns('',

	url(r'^$', RedirectView.as_view( url='home/') ),

	url(r'^static/', include('common.urls')),
	url(r'^account/', include('account.urls')),
	url(r'^org/', include('org.urls')),

	url(r'^timesheet/', include('timesheet.urls')),
	url(r'^home/', include('home.urls')),

	url(r'^admin/', include('admin.urls')),
)

