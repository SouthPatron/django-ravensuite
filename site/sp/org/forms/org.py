from django import forms

from common.models import *



class EditOrganization( forms.ModelForm ):
	class Meta:
		model = Organization
		exclude = ( 'refnum', )


