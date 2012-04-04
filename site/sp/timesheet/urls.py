from django.contrib.auth.decorators import login_required

from django.conf.urls import url, patterns
from django.conf import settings

from views import *

urlpatterns = patterns('',

	url( r'^entries$', login_required( EntryList.as_view() ), name = 'timesheet-entry-list' ),


	url( r'^timers$', login_required( TimerList.as_view() ), name = 'timesheet-timer-list' ),

	url( r'^timer/(?P<timerid>\d+)$', login_required( TimerSingle.as_view() ), name = 'timesheet-timer-single' ),

)


