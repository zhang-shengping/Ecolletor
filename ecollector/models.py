#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import *
from datetime import datetime

metadata = MetaData()

time = Table('time', metadata,
             Column('resource_id', String(255), index=True),
             Column('start_timestamp', DateTime()),
             Column('end_timestamp', DateTime()))

compute = Table('compute', metadata,
                Column('resource_id', String(255), index=True),
                Column('flavor', String(125)))

