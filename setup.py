from setuptools import setup

setup(
		name = 'django-sptools',
		version = '0.2.0',
		author = 'SouthPatron',
		author_email = 'support@southpatron.com',
		packages = [ 'sptools', ],
		url = 'http://www.southpatron.com',
		license = 'LICENSE.txt',
		description = 'SouthPatron Tools',
		long_description=open('README.txt').read(),
		install_requires=[
			"Django >= 1.4.0",
		]
	)

