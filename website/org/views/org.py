from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect

from singleobjectview import SingleObjectView
from listview import ListView

from ..models import *

class OrgList( ListView ):
	template_name = 'pages/org/org/index'

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = Organization.objects.all()
		return obj_list
	
	def create_object_json( self, request, data, *args, **kwargs ):

		neworg = Organization()
		neworg.trading_name = data[ 'trading_name' ]
		neworg.save()

		oid = neworg.id

		return redirect( 'org-single', oid = oid )


class OrgSingle( SingleObjectView ):
	template_name = 'pages/org/org/single'

	def get_object( self, request, *args, **kwargs ):
		oid = kwargs.get( 'oid', None )
		print 'oid = {}'.format( oid )
		if oid is None:
			self.not_found()

		return get_object_or_404( Organization, id = oid )



