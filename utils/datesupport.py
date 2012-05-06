from dbgdatetime import datetime


class DateSupport( object ):

	@staticmethod
	def get_days_in_month( sdate ):
		adate = datetime.date( year = sdate.year, month = sdate.month, day = 1 )
		if sdate.month == 12:
			bdate = datetime.date( year = sdate.year + 1, month = 1, day = 1 )
		else:
			bdate = datetime.date( year = sdate.year, month = sdate.month + 1, day = 1 )
		return (bdate - adate).days

	@staticmethod
	def get_first_day_of_month( sdate ):
		return datetime.date( year = sdate.year, month = sdate.month, day = 1 )


	@staticmethod
	def get_first_day_of_next_month( sdate ):
		if sdate.month == 12:
			return datetime.date( year = sdate.year + 1, month = 1, day = 1 )
		else:
			return datetime.date( year = sdate.year, month = sdate.month + 1, day = 1 )

	@staticmethod
	def get_last_day_of_month( sdate ):
		return DateSupport.get_first_day_of_next_month( sdate ) - datetime.timedelta( 1 )

	@staticmethod
	def get_first_day_of_previous_month( sdate ):
		return DateSupport.get_first_day_of_month( DateSupport.get_first_day_of_month( sdate ) - datetime.timedelta( 1 ) )

	@staticmethod
	def get_last_day_of_previous_month( sdate ):
		return DateSupport.get_first_day_of_month( sdate ) - datetime.timedelta( 1 )




