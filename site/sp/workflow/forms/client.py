from django import forms

from workflow.models import *



class EditClient( forms.ModelForm ):
	class Meta:
		model = Client
		exclude = ( 'organization', 'refnum', 'state' )



