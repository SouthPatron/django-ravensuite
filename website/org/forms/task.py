from django import forms

from ..models import *



class CreateTask( forms.ModelForm ):
	class Meta:
		model = Task
		exclude = ( 'activity', )


