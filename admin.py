from django.db.models import get_models, get_app
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from common.models import *


# ------------- Admin Classes go here. Automatically loaded by autoregister


class OrganizationAdmin( admin.ModelAdmin ):
	readonly_fields = ( 'refnum', )
	list_display = ( 'trading_name', 'refnum' )

class OrganizationAccountAdmin( admin.ModelAdmin ):
	readonly_fields = ( 'organization', )
	list_display = ( 'organization', )

class OrganizationCounterAdmin( admin.ModelAdmin ):
	readonly_fields = ( 'organization', 'source_document_no', 'client_no', 'project_no' )
	list_display = ( 'organization', )

class OrganizationSettingsAdmin( admin.ModelAdmin ):
	readonly_fields = ( 'organization', )
	list_display = ( 'organization', )

class AuthenticationCodeAdmin( admin.ModelAdmin ):
	readonly_fields = ( 'user', )
	list_display = ( 'user', 'creation_time', 'authentication_code' )

class UserMembershipAdmin( admin.ModelAdmin ):
	readonly_fields = ( 'user', 'organization' )
	list_display = ( 'user', 'organization', 'category', 'is_enabled' )
	list_display_links = ( 'category', )

class ClientAdmin( admin.ModelAdmin ):
	readonly_fields = ( 'organization', 'refnum' )
	list_display = ( 'organization', 'refnum', 'trading_name' )
	list_display_links = ( 'trading_name', )

class AccountAdmin( admin.ModelAdmin ):
	readonly_fields = ( 'client', 'transaction_no', 'balance' )
	list_display = ( 'client', 'transaction_no', 'balance' )
	list_display_links = ( 'balance', )

class SourceDocumentAdmin( admin.ModelAdmin ):
	readonly_fields = ( 'client', 'refnum', 'creation_time', 'event_time', 'document_type', 'document_state', 'amount', 'tax', 'total', 'allocated' )
	list_display = ( 'refnum', 'client', 'document_type', 'document_state', 'total'  )
	list_display_links = ( 'refnum', )

class ActivityAdmin( admin.ModelAdmin ):
	readonly_fields = ( 'organization', )
	list_display = ( 'organization', 'name' )
	list_display_links = ( 'name', )

class TaskAdmin( admin.ModelAdmin ):
	readonly_fields = ( 'activity', )
	list_display = ( 'activity', 'name' )
	list_display_links = ( 'name', )

class ProjectAdmin( admin.ModelAdmin ):
	readonly_fields = ( 'client', 'refnum' )
	list_display = ( 'refnum', 'client', 'name', 'status' )
	list_display_links = ( 'name', )

# ------------- AutoRegister the common app ----------------------

def autoregister(*app_list):
	for app_name in app_list:
		app_models = get_app(app_name)
		for model in get_models(app_models):
			try:
				adminClass = None

				try:
					# See if there is an Admin object
					import sys
					modname = globals()['__name__']
					module = sys.modules[ modname ]

					adminClass = getattr( module,
									'{}Admin'.format( model.__name__ )
								)
				except AttributeError:
					pass
					
				admin.site.register( model, adminClass )
			except AlreadyRegistered:
				pass

autoregister( 'common' )


