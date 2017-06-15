#!/usr/bin/env python
# encoding: utf-8

import datetime

def unix_to_strtime(time):
    strtime = datetime.datetime.fromtimestamp(
        time
    ).strftime('%Y-%m-%dT%H:%M:%SZ')

    return strtime

def str_to_unixtime(time):
    pass

