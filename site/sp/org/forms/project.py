from django import forms

from common.models import *



class CreateProject( forms.ModelForm ):
	class Meta:
		model = Project
		exclude = ( 'client', 'refnum' )


