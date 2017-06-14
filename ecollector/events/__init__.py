#!/usr/bin/env python
# encoding: utf-8

import abc

class Event(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def resource_id():
        pass

    @abc.abstractproperty
    def end_timestamp():
        pass

    @abc.abstractproperty
    def start_timestamp():
        pass

    @classmethod
    def collect_events():
        pass
