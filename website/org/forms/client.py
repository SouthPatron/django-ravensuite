from django import forms

from common.models import *



class AddClient( forms.ModelForm ):
	class Meta:
		model = Client
		exclude = ( 'organization', 'refnum', )



