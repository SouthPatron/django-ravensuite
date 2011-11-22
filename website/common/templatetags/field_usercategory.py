from django import template

from ..models import *

register = template.Library()

@register.simple_tag
def field_usercategory( code ):
	return UserCategory.get( code )[1]



