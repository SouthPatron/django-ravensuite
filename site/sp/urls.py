from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

	url(r'^$', RedirectView.as_view( url='home/') ),

	url(r'^static/', include('common.urls')),
	url(r'^account/', include('sp.account.urls')),
	url(r'^org/', include('sp.org.urls')),
	url(r'^timesheet/', include('sp.timesheet.urls')),
	url(r'^home/', include('sp.home.urls')),

	url(r'^favicon\.ico$',
			RedirectView.as_view( url='/static/local/images/favicon.ico' )
		),

	url(r'^restart$',
			'common.views.helps.restart'
		),


	# Built-in Django admin tools
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls))

)

