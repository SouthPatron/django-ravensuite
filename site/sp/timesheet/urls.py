from django.contrib.auth.decorators import login_required

from django.conf.urls import url, patterns
from django.conf import settings

from views import *

from common.views.modal import ModalView


urlpatterns = patterns('',

	url( r'^$', login_required( TimesheetEntryList.as_view() ), name = 'timesheet-entry-list' ),


	url( r'^modals/(?P<modal_name>.*)$', login_required( ModalView.as_view() ) ),

)


