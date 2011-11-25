from django.contrib.auth.decorators import login_required

from django.conf.urls.defaults import *
from django.conf import settings

from views import *

urlpatterns = patterns('',

	url( r'^$', login_required( EntryList.as_view() ), name = 'timesheet-entry-list' ),

)


