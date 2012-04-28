from django.contrib.auth.decorators import login_required

from django.conf.urls import url, patterns
from django.conf import settings

from common.views.restfulview import RestfulView

from api_restful import restful_list


urlpatterns = patterns('',

	url( r'^restful/(?P<node>.*)\.(?P<api_format>\w+)$', login_required( RestfulView.as_view( base_module = 'sp.contacts.api.restful', restful_list = restful_list ) ) ),
	url( r'^restful/(?P<node>.*)$', login_required( RestfulView.as_view( base_module = 'sp.contacts.api.restful', restful_list = restful_list ) ) ),

)


