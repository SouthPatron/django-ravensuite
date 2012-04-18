from django.contrib.auth.decorators import login_required

from django.conf.urls import url, patterns
from django.conf import settings

from views import *


urlpatterns = patterns('',

	url( r'^restful/(?P<node>.*)\.(?P<api_format>\w+)$', login_required( RestfulDispatcher.as_view() ) ),
	url( r'^restful/(?P<node>.*)$', login_required( RestfulDispatcher.as_view() ) ),

)


