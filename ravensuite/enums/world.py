# -*- coding: utf-8 -*-

from ravensuite.utils.enum import ChoicesEnum
import pytz

CountryList = ChoicesEnum()

for cn in pytz.country_names:
	CountryList.set( cn, ( cn, pytz.country_names[cn] ) )


TimezoneList = ChoicesEnum()

for cn in pytz.common_timezones:
	TimezoneList.set( cn, ( cn, cn ) )



