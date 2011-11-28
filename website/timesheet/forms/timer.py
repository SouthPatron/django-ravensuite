from django import forms

from common.models import *


class NewTimer( forms.Form ):
	organization = forms.IntegerField()
	client = forms.IntegerField()
	project = forms.IntegerField()
	activity = forms.IntegerField()
	task = forms.IntegerField()
	description = forms.CharField( max_length = 255 )


