from django import forms

from common.models import *



class CreateTask( forms.ModelForm ):
	class Meta:
		model = Task
		exclude = ( 'activity', )


