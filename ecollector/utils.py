#!/usr/bin/env python
# encoding: utf-8

import datetime

def time_to_str(time, period=None):
    if period != None:
        endtime = time - datetime.timedelta(
            seconds=period)
        return endtime.strftime(
            '%Y-%m-%dT%H:%M:%SZ')
    return time.strftime('%Y-%m-%dT%H:%M:%SZ')
