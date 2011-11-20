from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseServerError

from singleobjectview import SingleObjectView
from listview import ListView

from common.models import *
from common.utils.dbgdatetime import datetime

class InvoiceList( ListView ):
	template_name = 'pages/org/invoice/index'

	def get_object_list( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'aid' ], **kwargs )

		obj_list = Invoice.objects.filter( account__refnum = mid.aid, account__client__refnum = mid.cid, account__client__organization__refnum = mid.oid )
		return obj_list
	
	def create_object_json( self, request, data, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'aid' ], **kwargs )

		# TODO: select_for_update()
		orgcounter = OrganizationCounter.objects.get( organization__refnum = mid.oid )

		# TODO: select_for_update()
		theaccount = Account.objects.get( refnum = mid.aid )

		if theaccount.is_enabled is False:
			return HttpResponseForbidden()

		newt = Invoice()
		newt.account = theaccount
		newt.refnum = orgcounter.invoice_no
		newt.creation_time = datetime.datetime.now()
		newt.invoice_date = datetime.date.today()
		newt.due_date = datetime.date.today()
		newt.state = State.DRAFT
		newt.save()

		orgcounter.invoice_no += 1
		orgcounter.save()

		return redirect( 'org-client-account-invoice-single', oid = mid.oid, cid = mid.cid, aid = mid.aid, iid = newt.refnum )


class InvoiceSingle( SingleObjectView ):
	template_name = 'pages/org/transaction/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'aid', 'iid' ], **kwargs )
		return get_object_or_404( Invoice, refnum = mid.iid, account__refnum = mid.aid, account__client__refnum = mid.cid, account__client__organization__refnum = mid.oid )

	def delete_object( self, request, ob, *args, **kwargs ):
		if ob.state == State.FINAL:
			return HttpResponseForbidden()

		ob.delete()
		return redirect( 'org-client-account-invoice-list', cid = ob.account.client.refnum, oid = ob.account.client.organization.refnum, aid = ob.account.refnum )


	def void_invoice( self, request, obj, data, *args, **kwargs ):

		return redirect( 'org-client-account-invoice-single', oid = obj.account.client.organization.refnum, cid = obj.account.client.refnum, aid = obj.account.refnum, iid = obj.refnum )

	def finalize_invoice( self, request, obj, data, *args, **kwargs ):

		return redirect( 'org-client-account-invoice-single', oid = obj.account.client.organization.refnum, cid = obj.account.client.refnum, aid = obj.account.refnum, iid = obj.refnum )

	def update_invoice( self, request, obj, data, *args, **kwargs ):
		obj.invoice_date = data.get( 'invoice_date', obj.invoice_date )
		obj.due_date = data.get( 'due_date', obj.due_date )
		obj.save()

		return redirect( 'org-client-account-invoice-single', oid = obj.account.client.organization.refnum, cid = obj.account.client.refnum, aid = obj.account.refnum, iid = obj.refnum )


	def update_object_json( self, request, obj, data, *args, **kwargs ):

		newstate = data.get( 'state', None )

		if newstate is not None:
			if State.contains( newstate ) is False:
				return HttpResponseForbidden()

			if obj.state == State.FINAL:
				if newstate != State.VOID:
					return HttpResponseForbidden()
				return void_invoice( request, obj, data, *args, **kwargs )

			if newstate == State.VOID:
				return delete_object( request, obj, data, *args, **kwargs )

			if newstate == State.FINAL:
				return finalize_invoice( request, obj, data, *args, **kwargs )

			return HttpResponseServerError()

		return update_invoice( request, obj, data, *args, **kwargs )

