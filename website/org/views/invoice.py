from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseServerError

from common.views.singleobjectview import SingleObjectView
from common.views.listview import ListView

from common.models import *
from common.utils.dbgdatetime import datetime

class InvoiceList( ListView ):
	template_name = 'pages/org/invoice/index'

	def get_extra( self, request, obj_list, fmt, *args, **kwargs ):
		return Account.objects.get( refnum = self.url_kwargs.aid, client__refnum = self.url_kwargs.cid, client__organization__refnum = self.url_kwargs.oid )

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
		newt.state = InvoiceState.DRAFT
		newt.save()

		orgcounter.invoice_no += 1
		orgcounter.save()

		resp = { 'url' : newt.get_single_url() }
		return self.api_resp( resp )


class InvoiceSingle( SingleObjectView ):
	template_name = 'pages/org/invoice/single'

	def get_object( self, request, *args, **kwargs ):
		mid = self._extract_ids( [ 'oid', 'cid', 'aid', 'iid' ], **kwargs )
		return get_object_or_404( Invoice, refnum = mid.iid, account__refnum = mid.aid, account__client__refnum = mid.cid, account__client__organization__refnum = mid.oid )

	def delete_object( self, request, ob, *args, **kwargs ):
		if ob.state == InvoiceState.FINAL:
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


	def update_object_html( self, request, obj, data, *args, **kwargs ):

		invoice_data = {}

		invoice_data[ 'invoice_date' ] = data.get( 'invoice_date' )
		invoice_data[ 'due_date' ] = data.get( 'due_date' )
		invoice_data[ 'tax' ] = data.get( 'invoice_tax' )
		invoice_data[ 'amount' ] = data.get( 'invoice_amount' )
		invoice_data[ 'total' ] = data.get( 'invoice_total' )
		invoice_data[ 'comment' ] = data.get( 'invoice_comment', "" )

		invoice_data[ 'state' ] = data.get( 'invoice_state' )

		invoice_data[ 'items' ] = []
		
		for pos in range( len(data.getlist( 'description' )) ):
			invoice_data[ 'items' ].append( [
						data.getlist( 'description' )[ pos ],
						data.getlist( 'units' )[ pos ],
						data.getlist( 'perunit' )[ pos ],
						data.getlist( 'tax_rate' )[ pos ],
						data.getlist( 'amount' )[ pos ]
					] )


		print invoice_data;

		return redirect( obj.get_single_url() )


	def update_object_json( self, request, obj, data, *args, **kwargs ):

		newstate = data.get( 'state', None )

		if newstate is not None:
			if InvoiceState.contains( newstate ) is False:
				return HttpResponseForbidden()

			if obj.state == InvoiceState.FINAL:
				if newstate != InvoiceState.VOID:
					return HttpResponseForbidden()
				return void_invoice( request, obj, data, *args, **kwargs )

			if newstate == InvoiceState.VOID:
				return delete_object( request, obj, data, *args, **kwargs )

			if newstate == InvoiceState.FINAL:
				return finalize_invoice( request, obj, data, *args, **kwargs )

			return HttpResponseServerError()

		return update_invoice( request, obj, data, *args, **kwargs )

