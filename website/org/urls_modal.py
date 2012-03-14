from django.contrib.auth.decorators import login_required

from django.conf.urls.defaults import *
from django.conf import settings

from common.views.modal import ModalView

from modals import *


urlpatterns = patterns('',

	url( r'^(?P<modal_name>org\.new\.organization)$', login_required( ModalView.as_view( logic_class = NewOrganization ) ), name = 'org-modal-new-organization' ),

)


