#!/usr/bin/env python
# encoding: utf-8

from ceilometerclient import client as cclient
from keystoneauth1 import loading as ks_loading
from keystoneclient.v3 import client as kclient

from ecollector import convertor

from oslo_config import cfg
# import abc

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
    # __metaclass__ = abc.ABCMeta

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

        self._conn = None

class ProjectCollector(BaseCollector):

    def __init__(self):
        super(ProjectCollector, self).__init__()
        self._conn = kclient.Client(session=self.session)

    def get_projects(self):
        projects = self._conn.projects.list()
        return projects

    def get_users(self):
        users = self._conn.users.list()
        return users



class StatCollector(BaseCollector):

    def __init__(self):
        super(StatCollector, self).__init__()
        self._conn = cclient.get_client('2', session=self.session)

    def get_resources(self,
                      meter,
                      start=None,
                      end=None,
                      project_id=None,
                      q_filter=None,
                      aggre=None):
        # [{'field': 'timestamp', 'value': '2017-06-07T01:00:00Z', 'op': 'ge'},
        # {'field': 'project', 'value': u'8ab00ca9c3414762b5aa598b37b5a567', 'op': 'eq'},
        # {'field': 'timestamp', 'value': '2017-06-07T02:00:00Z', 'op': 'le'}]
        query_filter = []
        if project_id:
            query_filter.append({'field':'project',
                                 'op':'eq',
                                 'value':project_id})
        if start:
            query_filter.append({'field':'timestamp',
                                 'op':'ge',
                                 'value':start})
        if end:
            query_filter.append({'field':'timestamp',
                                 'op':'le',
                                 'value':end})

        if isinstance(q_filter, list):
            query_filter += q_filter
        else:
            # len([None]) is 1
            # len([None]) is not equal None
            if q_filter:
                query_filter.append(q_filter)

        resources = self._conn.statistics.list(meter_name=meter,
                                               period=0,
                                               groupby=['resource_id'],
                                               q=query_filter,
                                               aggregates=aggre)

        return resources

    def get_resources_ids(self,
                          meter,
                          start=None,
                          end=None,
                          project_id=None,
                          q_filter=None,
                          aggre=None):

        resources = self.get_resources('instance',
                                       start=start,
                                       end=end,
                                       project_id=project_id)

        return [resource.groupby['resource_id']
                for resource in resources]

    def get_compute(self, project_id, start=None, end=None):

        resource_ids = self.get_resources_ids('instance',
                                              start,
                                              end,
                                              project_id)

        resources = {}
        for _id in resource_ids:
            _resource = self._conn.resources.get(_id)
            resources[_id] = _resource

        return resources


    def get_network(self, project_id, start=None, end=None):
        pass


if __name__ == "__main__":
    from oslo_config import cfg
    cfg.CONF(project='ecollector')

    #b = StatCollector()
    #data = b.get_compute(start = '2017-06-07T01:00:00',
                         # end = '2017-06-07T02:00:00',
                         # project_id='8ab00ca9c3414762b5aa598b37b5a567')
    # print data

    k = ProjectCollector()
    #u = k.get_users()
    projects_list = k.get_projects()
    print projects_list




