from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

	url(r'^$', RedirectView.as_view( url='home/') ),

	url(r'^api/', include('sp.api.urls') ),

	url(r'^static/', include('common.urls')),
	url(r'^favicon\.ico$',
			RedirectView.as_view( url='/static/local/images/favicon.ico' )
		),

	url(r'^restart$', 'common.views.helps.restart' ),

	url(r'^v/account/', include('sp.account.urls')),
	url(r'^v/org/', include('sp.org.urls')),
	url(r'^v/timesheet/', include('sp.timesheet.urls')),

	# Built-in Django admin tools
	url(r'^v/admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^v/admin/', include(admin.site.urls))

)


