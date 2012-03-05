from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
	url(r'^static/', include('common.urls')),
	url(r'^account/', include('account.urls')),
	url(r'^org/', include('org.urls')),
	url(r'^timesheet/', include('timesheet.urls')),
)

