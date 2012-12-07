from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template
from django.template import Context

import copy


def build_address( user ):
	return '"{} {}" <{}>'.format(
				user.first_name,
				user.last_name,
				user.email )



def send_templated_email( template_name, from_address, keys = {}, cc_list = [], bcc_list = [], to_list = [], user = None ):

	t_subject = get_template( '{}.subject'.format( template_name ) )
	t_text = get_template( '{}.txt'.format( template_name ) )
	t_html = get_template( '{}.html'.format( template_name ) )

	dkey = copy.deepcopy( keys )
	dkey[ 'user' ] = user

	d = Context( dkey )

	subject = t_subject.render(d).replace( '\n', '' ).replace( '\r', '' )

	if user is not None:
		if len(to_list) != 0:
			raise RuntimeError( 'user or to_list, you have to choose one' )
		tol = [ build_address( user ), ]
	else:
		tol = to_list

	msg = EmailMultiAlternatives(
				subject = subject,
				body = t_text.render(d),
				from_email = from_address,
				to = tol,
				bcc = bcc_list,
				cc = cc_list,
			)
	msg.attach_alternative( t_html.render(d), "text/html" )
	msg.send()


