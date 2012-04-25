from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

from common.views.directtemplate import direct_template
from common.views.modal import ModalView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

	url(r'^$', RedirectView.as_view( url='home/') ),
	url(r'^home/', direct_template ),

	url(r'^api/', include('sp.api.urls') ),
	url( r'^modals/(?P<modal_name>.*)$', login_required( ModalView.as_view() ) ),

	url(r'^static/', include('common.urls')),
	url(r'^favicon\.ico$',
			RedirectView.as_view( url='/static/local/images/favicon.ico' )
		),


	url(r'^account/', include('account.urls')),

	url(r'^v/(?P<oid>\w{32})/workflow', include('sp.workflow.urls')),
	url(r'^v/(?P<oid>\w{32})/accounting', include('sp.accounting.urls')),
	url(r'^v/(?P<oid>\w{32})/contacts', include('sp.contacts.urls')),

	# Built-in Django admin tools
	url(r'^v/admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^v/admin/', include(admin.site.urls)),

	url(r'^restart$', 'common.views.helps.restart' ),

)


