from django import forms

from workflow.models import *



class CreateProject( forms.ModelForm ):
	class Meta:
		model = Project
		exclude = ( 'client', 'refnum' )


