from django import forms

from workflow.models import *



class CreateTask( forms.ModelForm ):
	class Meta:
		model = Task
		exclude = ( 'activity', )


