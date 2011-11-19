from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template
from django.template import Context


FROM_ADDRESS = '"Support at SMK" <support@smksoftware.com>'


def send_templated_email( user, app, template_name, keys = {} ):

	template_subject = get_template( 'emails/{}/{}.subject'.format( app, template_name ) )
	template_text = get_template( 'emails/{}/{}.txt'.format( app, template_name ) )
	template_html = get_template( 'emails/{}/{}.html'.format( app, template_name ) )

	dkey = keys
	dkey[ 'user' ] = user

	d = Context( dkey )

	text_content = template_text.render(d)
	html_content = template_html.render(d)

	subject = template_subject.render(d)
	subject = subject.replace( '\n', '' ).replace( '\r', '' )

	from_email = FROM_ADDRESS
	to_email = '"' + user.first_name + ' ' + user.last_name + '" <' + user.email + '>'

	msg = EmailMultiAlternatives( subject, text_content, from_email, [to_email] )
	msg.attach_alternative( html_content, "text/html" )
	msg.send()


