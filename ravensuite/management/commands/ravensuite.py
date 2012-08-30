from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
	args = '<function_name> [ application application ... ]'
	help = 'Runs the function name from rs.py in each - or all if none - specified application'

	def handle(self, *args, **options):

		if len( args ) < 1:
			raise CommandError( 'No function name specified' )

		fname = args[0]

		if len( args ) < 2:
			applist = settings.INSTALLED_APPS
		else:
			applist = args[1:]

		for app in applist:
			try:
				name = app + '.rs'
				mod = __import__( name, fromlist=[] )
				components = name.split( '.' )
				components.append( fname )
				for comp in components[1:]:
					mod = getattr(mod, comp)
				print 'Running: {}.{}'.format( name, fname )
				mod()
			except ImportError:
				pass
			except AttributeError:
				pass



