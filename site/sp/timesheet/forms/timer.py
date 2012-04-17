from django import forms

from common.models import *


class NewTimer( forms.ModelForm ):
	class Meta:
		model = TimesheetEntry
		exclude = ( 'user', 'seconds' )


	def __init__( self, *args, **kwargs ):
		super( NewTimer, self ).__init__( *args, **kwargs )
		self.empty_label = 'dougie'



