from __future__ import unicode_literals

from django.shortcuts import get_object_or_404


from ..models import *
from base import Base

class Org( Base ):
	template_name = 'pages/org/org/index'

	def get_object( self, request, *args, **kwargs ):
		pk = kwargs.get( 'pk', None )
		if pk is None:
			self.not_found()

		return get_object_or_404( Organization, id = pk )



