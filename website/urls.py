from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

	url(r'^account/', include('account.urls')),
	url(r'^org/', include('org.urls')),
	url(r'^timesheet/', include('timesheet.urls')),

)

