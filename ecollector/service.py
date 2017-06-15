#!/usr/bin/env python
# encoding: utf-8

from ecollector.collector import ProjectCollector
from ecollector.collector import StatCollector
from ecollector import utils
from oslo_config import cfg
# import datetime
import time
import cotyledon
import logging

#LOG = logging.getLogger("cotyledon.tests.examples")
logging.basicConfig(level=logging.WARN)
LOG = logging.getLogger(__name__)

OPTS = [
    cfg.IntOpt('period',
               default = 3600,
               help = 'collect data period')
]

cfg.CONF.register_opts(OPTS, group='collector')

class CollectService(cotyledon.Service):

    def __init__(self, worker_id):
        super(CollectService, self).__init__(worker_id)
        self.running = True
        self.id = worker_id


    def run(self):
        projects_collector = ProjectCollector()
        LOG.warn('auth_url is %s', cfg.CONF.service_credentials.auth_url)
        projects_collector.get_projects()
        start = time.time()
        period = cfg.CONF.collector.period
        end = start + period
        start_timestamp = utils.unix_to_strtime(start)
        end_timestamp = utils.unix_to_strtime(end)
        LOG.warn("start_time: %s"%start_timestamp)
        LOG.warn("end_time: %s"%end_timestamp)
        # while self.running:
            # projects_collector = ProjectCollector()
            # stat_collector = StatCollector()

            # start = time.time()
            # period = cfg.CONF.collector.period
            # end = start + period

            # start_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", start)
            # end_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", end)

            # projects = projects_collector.get_projects()
            # for _proj in projects:
                # resources = stat_collector.get_compute(
                    # project_id=_proj.id,
                    # start=start_timestamp,
                    # end=end_timestamp
                # )

            # time.sleep(3600)
            # print resources

    def terminate(self):
        self.running = False

    def reload(self):
        print "reload {} process".format(self.id)

class Manager(cotyledon.ServiceManager):
    def __init__(self):
        super(Manager, self).__init__()
        #self.register_hooks(on_reload=self.reload)
        self.service_id = self.add(CollectService, 1)



if __name__ == "__main__":
    cfg.CONF(project='ecollector')
    manager = cotyledon.ServiceManager()
    manager.add(CollectService, workers=1)
    manager.run()
    # cfg.CONF(project='ecollector')
    # m = Manager()
    # m.run()
