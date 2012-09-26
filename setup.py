from setuptools import setup

setup(
		name = 'django-ravensuite',
		version = '0.2.19',
		author = 'SMK Software',
		author_email = 'support@smksoftware.com',
		packages = [ 'ravensuite', ],
		url = 'http://www.smksoftware.com',
		license = 'LICENSE.txt',
		description = 'Ravensuite',
		long_description=open('README.txt').read(),
		install_requires=[
			"Django >= 1.4.0",
			"slimit >= 0.7.4"
		]
	)

