from django import template

import hashlib
import urllib

register = template.Library()

@register.tag(name='gravatar')
def do_gravatar(parser, token):
	vals = token.split_contents()

	if len( vals ) < 2:
		raise template.TemplateSyntaxError("'gravatar' node requires aleast a username parameter.")

	if len( vals ) == 2:
		return GravatarNode( username = vals[1] )

	if len( vals ) == 3:
		return GravatarNode( username = vals[1], size = vals[2] )

	if len( vals ) == 4:
		return GravatarNode( username = vals[1], size = vals[2], default=vals[3] )

	raise template.TemplateSyntaxError("'gravatar' node received too many parameters.")

class GravatarNode( template.Node ):
	def __init__( self, username, size = None, default = None ):
		self.username = template.Variable( username )
		self.size = size
		self.default = default


	def render(self, context):
		username = self.username.resolve( context )

		if self.size is not None:
			size = int(template.Variable( self.size ).resolve( context ))
		else:
			size = 64

		if self.default is not None:
			default = template.Variable( self.default ).resolve( context )
		else:
			# default = '/images/icons/user.png' 
			default = 'mm' 

		md5sum = hashlib.md5()
		md5sum.update( username.strip().lower() )

		return 'http://www.gravatar.com/avatar/{}.jpg?{}'.format( md5sum.hexdigest(), urllib.urlencode( {'s':str(size),'d':default} ) )


