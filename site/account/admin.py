from django.db.models import get_models, get_app
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from models import *


# ------------- Admin Classes go here. Automatically loaded by autoregister


class OrganizationAdmin( admin.ModelAdmin ):
	readonly_fields = ( 'refnum', )
	list_display = ( 'trading_name', 'refnum' )


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

autoregister( 'account' )

