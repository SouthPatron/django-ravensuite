DT = __import__( 'datetime' )

from ..models import DebugControl


class datetime( object ):
	debug_mode = True

	class datetime( DT.datetime ):

		@staticmethod
		def now():
			if datetime.debug_mode is False:
				return DT.datetime.now()

			try:
				dbg = DebugControl.objects.get( id = 1 )
			except DebugControl.DoesNotExist:
				return DT.datetime.now()

			return dbg.current_time

	class date( DT.date ):

		@staticmethod
		def today():
			if datetime.debug_mode is False:
				return DT.date.today()

			try:
				dbg = DebugControl.objects.get( id = 1 )
			except DebugControl.DoesNotExist:
				return DT.datetime.now()

			return dbg.current_time.date()

	class timedelta( DT.timedelta ):
		pass

