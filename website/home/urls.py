
from django.conf.urls.defaults import patterns, url, include
from django.views.generic import TemplateView


urlpatterns = patterns('',

	url( r'^$',
		TemplateView.as_view(template_name='pages/home/index.html'),
		name = 'home-index'
	),

)

