from __future__ import unicode_literals

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.views.generic.edit import ProcessFormView

import subprocess


class UpdateView( ProcessFormView ):

	template_name = 'pages/admin/shell.html'

	def get( self, request, *args, **kwargs ):
		response = render_to_response(
					self.template_name,
					{
						'output' : ''
					},
					context_instance=RequestContext(request)
				)
		return response


	def post( self, request, *args, **kwargs ):

		output = ''

		if request.method == 'POST' and request.POST != None:
			cmd = request.POST[ 'command' ]

			try:
				output = subprocess.check_output( cmd, shell = True )
			except subprocess.CalledProcessError, e:
				output = e.message()
			


		response = render_to_response(
					self.template_name,
					{
						'output' : output
					},
					context_instance=RequestContext(request)
				)
		return response


