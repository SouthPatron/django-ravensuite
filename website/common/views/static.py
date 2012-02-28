from __future__ import unicode_literals

import re

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.conf import settings

from django.views.static import serve



def static_serve( request, path_name ):

	mo = re.match( r"^local\/css\/.*$", path_name )

	if mo is None:
		return serve(
				request,
				path = path_name,
				document_root = settings.STATIC_BASE,
				show_indexes = False
			)

	return render_to_response(
				'static/{}'.format( path_name ),
				{ },
				context_instance=RequestContext(request),
				mimetype='text/css'
			)




