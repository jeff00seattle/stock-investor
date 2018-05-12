#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import datetime as dt

# requires python-dateutil (http://labix.org/python-dateutil)
from dateutil.relativedelta import relativedelta

def month_day_range(month_datetime):
    """
    For a date 'date' returns the start and end date for the month of 'date'.
    Month with 31 days:
    >>> date = dt.date(2011, 7, 27)
    >>> month_day_range(date)
    (datetime.date(2011, 7, 1), datetime.date(2011, 7, 31))
    Month with 28 days:
    >>> date = dt.date(2011, 2, 15)
    >>> month_day_range(date)
    (datetime.date(2011, 2, 1), datetime.date(2011, 2, 28))
    """
    month_date = dt.datetime.strptime(month_datetime, "%Y-%m") if isinstance(month_datetime, str) else month_datetime
    last_day = month_date + relativedelta(day=1, months=+1, days=-1)
    first_day = month_date + relativedelta(day=1)
    return first_day, last_day