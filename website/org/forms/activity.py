from django import forms

from ..models import *



class CreateActivity( forms.ModelForm ):
	class Meta:
		model = Activity
		exclude = ( 'organization', )


