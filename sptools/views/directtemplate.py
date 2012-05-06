from __future__ import unicode_literals

from django.shortcuts import render_to_response
from django.template import RequestContext, TemplateDoesNotExist

import re

def direct_template( request ):
	node = request.path_info

	converted = False

	if re.match( r"^.*\/$", node ) is not None:
		node = '{}index'.format( node )
		converted = True

	try:
		return render_to_response(
					'pages{}.html'.format( node ),
					{
					},
					context_instance=RequestContext(request)
				)
	except TemplateDoesNotExist:
		if converted is True:
			raise

		node = '{}/index'.format( node )
		return render_to_response(
				'pages{}.html'.format( node ),
				{
				},
				context_instance=RequestContext(request)
			)

