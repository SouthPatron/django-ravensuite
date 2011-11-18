from django import forms

from ..models import *



class CreateTab( forms.ModelForm ):
	class Meta:
		model = Tab
		exclude = (
			'client',
			'refnum',
			'transaction_no',
			'is_enabled',
			'balance',
			'reserved',
			)

