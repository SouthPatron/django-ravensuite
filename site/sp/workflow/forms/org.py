from django import forms

from workflow.models import *



class EditOrganization( forms.ModelForm ):
	class Meta:
		model = Organization
		exclude = ( 'refnum', 'state', )


