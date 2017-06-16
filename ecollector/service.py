#!/usr/bin/env python
# encoding: utf-8

from ecollector.collector import ProjectCollector
from ecollector.collector import StatCollector
from ecollector import utils
from oslo_config import cfg
import datetime
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
        while self.running:
            projects_collector = ProjectCollector()
            stat_collector = StatCollector()

            # Ceilometer use UTC time,not localtime
            start = datetime.datetime.utcnow()
            period = cfg.CONF.collector.period

            start_timestamp = utils.time_to_str(start, period)
            end_timestamp = utils.time_to_str(start)

            projects = projects_collector.get_projects()
            print len(projects)
            print start_timestamp
            print end_timestamp

            for _proj in projects:
                resources = stat_collector.get_compute(
                    project_id=_proj.id,
                    start=start_timestamp,
                    end=end_timestamp
                )
                print resources
            self.running = False

            #time.sleep(3600)
            #print resources

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
