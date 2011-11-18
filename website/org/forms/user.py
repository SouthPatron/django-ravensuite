from django import forms

from ..models import *


class AddUser( forms.Form ):
	first_name = forms.CharField(
					required = True,
					min_length = 2,
					max_length = 32,
				)
	last_name = forms.CharField(
					required = True,
					min_length = 2,
					max_length = 32,
				)
	email_address = forms.EmailField(
						required = True,
					)

	category = forms.ChoiceField(
					required = True,
					choices = UserCategory.choices(),
				)


