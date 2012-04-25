from __future__ import unicode_literals

from django.db import models


class DebugControl( models.Model ):
	current_time = models.DateTimeField()


