from django import forms

from common.models import *


class NewTimer( forms.ModelForm ):
	class Meta:
		model = TimesheetTimer
		exclude = ( 'user', 'start_time' )


