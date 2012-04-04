from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView


urlpatterns = patterns('',

	url(r'^$', RedirectView.as_view( url='home/') ),

	url(r'^static/', include('common.urls')),
	url(r'^account/', include('sp.account.urls')),
	url(r'^org/', include('sp.org.urls')),
	url(r'^timesheet/', include('sp.timesheet.urls')),
	url(r'^home/', include('sp.home.urls')),
	url(r'^admin/', include('sp.admin.urls')),

	url(r'^favicon\.ico$',
			RedirectView.as_view( url='/static/local/images/favicon.ico' )
		),

	url(r'^restart$',
			'common.views.helps.restart'
		),



)

