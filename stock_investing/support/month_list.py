#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

def month_list(start_datetime, end_datetime):
    from dateutil.rrule import rrule, MONTHLY
    months = [dt.strftime("%Y-%m") for dt in rrule(MONTHLY, dtstart=start_datetime, until=end_datetime)]
    return months