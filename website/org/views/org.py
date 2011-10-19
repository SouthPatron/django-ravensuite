from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.conf import settings

from singleobjectview import SingleObjectView
from listview import ListView

from ..models import *


class OrgList( ListView ):
	template_name = 'pages/org/org/index'

	def get_object_list( self, request, *args, **kwargs ):
		obj_list = Organization.objects.all()
		return obj_list

	def create_object_html( self, request, data, *args, **kwargs ):

		# TODO: Use select_for_update()
		sc = SystemCounter.objects.get( id = 1 )
		refnum = sc.organization_no
		sc.organization_no += 1
		sc.save()

		neworg = Organization()
		neworg.trading_name = data[ 'trading_name' ]
		neworg.refnum = refnum
		neworg.save()

		OrganizationCounter.objects.create( organization = neworg )
		OrganizationAccount.objects.create( organization = neworg )

		return redirect( 'org-single', oid = refnum )

	
	def create_object_json( self, request, data, *args, **kwargs ):

		# TODO: Use select_for_update()
		sc = SystemCounter.objects.get( id = 1 )
		refnum = sc.organization_no
		sc.organization_no += 1
		sc.save()

		neworg = Organization()
		neworg.trading_name = data[ 'trading_name' ]
		neworg.refnum = refnum
		neworg.save()

		OrganizationCounter.objects.create( organization = neworg )
		OrganizationAccount.objects.create( organization = neworg )

		return redirect( 'org-single', oid = refnum )


class OrgSingle( SingleObjectView ):
	template_name = 'pages/org/org/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid' ], **kwargs )
		return get_object_or_404( Organization, refnum = mid.oid )

	def delete_object( self, request, ob, *args, **kwargs ):
		ob.delete()
		return redirect( 'org-list' )

	def update_object_json( self, request, obj, data, *args, **kwargs ):
		obj.trading_name = data.get( 'trading_name', obj.trading_name )
		obj.save()
		return redirect( 'org-single', oid = obj.refnum )

