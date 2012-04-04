from django.db.models import get_models, get_app
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from common.models import *


# ------------- Admin Classes go here. Automatically loaded by autoregister

class OrganizationAdmin( admin.ModelAdmin ):
	fieldsets = [
		( 'Howdy',
			{ 'fields': [ 'refnum', 'trading_name' ] } ),
		( 'The Rest',
			{ 'fields': [ 'telephone_number', 'fax_number', 'email_address', 'postal_address', 'physical_address' ] } ),
		]
	search_fields = ( 'trading_name', )


class AuthenticationCodeAdmin( admin.ModelAdmin ):
	list_display = ( 'user', 'creation_time', 'authentication_code' )




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


