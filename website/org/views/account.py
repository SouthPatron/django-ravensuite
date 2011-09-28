from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect

from singleobjectview import SingleObjectView
from listview import ListView

from ..models import *

class AccountList( ListView ):
	template_name = 'pages/org/account/index'

	def get_object_list( self, request, *args, **kwargs ):
		oid = kwargs.get( 'oid', None )
		if oid is None:
			self.not_found()

		cid = kwargs.get( 'cid', None )
		if cid is None:
			self.not_found()

		obj_list = Account.objects.filter( client = cid, client__organization = oid )
		return obj_list
	
	def create_object_json( self, request, data, *args, **kwargs ):
		print "Here we are"
		oid = kwargs.get( 'oid', None )
		if oid is None:
			self.not_found()

		cid = kwargs.get( 'cid', None )
		if cid is None:
			self.not_found()


		# TODO: select_for_update()
		sc = SystemCounter.objects.get( id = 1 )
		refnum = sc.account_no
		sc.account_no += 1
		sc.save()

		newacc = Account()
		newacc.client = Client.objects.get( id = cid )
		newacc.refnum = refnum
		newacc.is_enabled = data[ 'is_enabled' ]
		newacc.min_balance = data[ 'min_balance' ]
		newacc.name = data[ 'name' ]
		newacc.save()

		return redirect( 'org-client-account-single', oid = oid, cid = cid, aid = refnum )


class AccountSingle( SingleObjectView ):
	template_name = 'pages/org/account/single'

	def get_object( self, request, *args, **kwargs ):
		oid = kwargs.get( 'oid', None )
		if oid is None:
			self.not_found()

		cid = kwargs.get( 'cid', None )
		if cid is None:
			self.not_found()

		aid = kwargs.get( 'aid', None )
		if aid is None:
			self.not_found()

		return get_object_or_404( Account, refnum = aid, client = cid, client__organization = oid )



