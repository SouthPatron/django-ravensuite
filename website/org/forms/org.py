from django import forms

from common.models import *



class CreateOrganization( forms.ModelForm ):
	class Meta:
		model = Organization
		exclude = ( 'refnum', )


