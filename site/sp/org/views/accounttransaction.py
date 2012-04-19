from django.shortcuts import redirect

from common.views.pageview import PageView
from common.utils.dbgdatetime import datetime
from common.models import *

#from email.utils import parsedate_tz
#print parsedate_tz('Fri, 15 May 2009 17:58:28 +0700')

class AccountTransactionList( PageView ):
	template_name = 'pages/org/client/account/transaction/index'

	def get_object( self, request, *args, **kwargs ):
		return Account.objects.get( client__organization__refnum = self.url_kwargs.oid, client__refnum = self.url_kwargs.cid )

	def get_object_list( self, request, *args, **kwargs ):
		qd = request.GET or {}

		obj_list = AccountTransaction.objects.filter( account__client__refnum = self.url_kwargs.cid, account__client__organization__refnum = self.url_kwargs.oid ).order_by( '-event_time' )

		if qd.get( 'days', None ) is not None:
			now = datetime.date.today()
			now = now - datetime.timedelta( days = int(qd[ 'days' ]) )
			obj_list = obj_list.filter( event_time__gte = now )

		return obj_list


def account_transaction_router( request, oid, cid, tid ):
	actrans = AccountTransaction.objects.get( refnum = tid, account__client__refnum = cid, account__client__organization__refnum = oid )
	newobj = actrans.source_document
	return redirect( newobj.get_absolute_url() )

