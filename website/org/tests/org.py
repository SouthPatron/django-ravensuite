"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core import mail
from django.test import TestCase


class OrgIndex(TestCase):

	#fixtures = [ 'myfix1.json', 'myfix2.json' ]



	def testCreate(self):
		"""
		Tests that 1 + 1 always equals 2.
		"""
		self.assertEqual(1 + 1, 2)


		isTrue = self.client.login( username = '', password = '' )

#		self.assertEqual(len(mail.outbox), 1)
#		self.assertEqual(mail.outbox[0].subject, 'Subject here')


#		resp = self.client.put( '/arg/', { 'key' : 'value' } )

		# resp.content
		# resp.context
		# resp.status_code

		# self.assertEqual( resp.status_code, 200 )
		# self.assertRedirects(response, '/other/login/?next=/sekrit/')
		# selfassertContains(response, text, count=None, status_code=200, msg_prefix='')


#		isTrue = self.client.logout()

