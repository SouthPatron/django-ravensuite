from django import forms

from workflow.models import *



class CreateActivity( forms.ModelForm ):
	class Meta:
		model = Activity
		exclude = ( 'organization', )


