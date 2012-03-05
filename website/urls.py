from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

	url(r'^static/', include('website.common.urls')),

	url(r'^account/', include('website.account.urls')),
	url(r'^org/', include('website.org.urls')),
	url(r'^timesheet/', include('website.timesheet.urls')),
)

