from django import forms

from ..models import *



class CreateOrganization( forms.ModelForm ):
	class Meta:
		model = Organization
		exclude = ( 'refnum', )


