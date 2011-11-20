from django import forms

from common.models import *



class CreateAccount( forms.ModelForm ):
	class Meta:
		model = Account
		exclude = (
			'client',
			'refnum',
			'transaction_no',
			'is_enabled',
			'balance',
			)

