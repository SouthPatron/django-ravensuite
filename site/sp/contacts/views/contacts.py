from django.shortcuts import get_object_or_404, redirect

from account.views import AccountPageView

from sp.contacts.models import *


class ContactList( AccountPageView ):
	template_name = 'pages/contacts/contacts/index'


