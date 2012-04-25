from django.shortcuts import get_object_or_404, redirect

from account.views import AccountPageView

from sp.accounting.models import *


class Dashboard( AccountPageView ):
	template_name = 'pages/accounting/dashboard'


