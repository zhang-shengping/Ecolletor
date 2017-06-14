#!/usr/bin/env python
# encoding: utf-8

from ceilometerclient import client as cclient
from keystoneauth1 import loading as ks_loading
from oslo_config import cfg
#import abc

CRED = 'service_credentials'
ks_loading.register_session_conf_options(
    cfg.CONF,
    CRED
)
ks_loading.register_auth_conf_options(
    cfg.CONF,
    CRED
)

CONF = cfg.CONF

class BaseCollector(object):
    #__metaclass__ = abc.ABCMeta

    def __init__(self):

        self.auth = ks_loading.load_auth_from_conf_options(
            CONF,
            CRED
        )

        self.session = ks_loading.load_session_from_conf_options(
            CONF,
            CRED,
            auth=self.auth
        )

        import pdb; pdb.set_trace()
        self._conn = cclient.get_client('2', session=self.session)

#class MeterCollector(object):
#    pass

if __name__ == "__main__":
    from oslo_config import cfg
    cfg.CONF(project='ecollector')


    a = BaseCollector()
    c = a._conn



