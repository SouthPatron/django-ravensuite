from django import forms

from common.models import *



class CreateActivity( forms.ModelForm ):
	class Meta:
		model = Activity
		exclude = ( 'organization', )


