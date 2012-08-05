from setuptools import setup

setup(
		name = 'django-ravensuite',
		version = '0.2.2',
		author = 'SouthPatron',
		author_email = 'support@southpatron.com',
		packages = [ 'ravensuite', ],
		url = 'http://www.southpatron.com',
		license = 'LICENSE.txt',
		description = 'Ravensuite',
		long_description=open('README.txt').read(),
		install_requires=[
			"Django >= 1.4.0",
			"slimit >= 0.7.4"
		]
	)

