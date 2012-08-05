from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
	args = '<application application ...>'
	help = 'Parses the applications deploy.py for assets to deploy'

	def handle(self, *args, **options):

		for app in args:
			print 'Building app: ' + app



