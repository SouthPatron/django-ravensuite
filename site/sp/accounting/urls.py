from django.contrib.auth.decorators import login_required

from django.conf.urls import url, patterns
from django.conf import settings

from views import *


urlpatterns = patterns('',

	url( r'^$', login_required( Dashboard.as_view() ), name = 'accounting-dashboard' ),

)


