#!/usr/bin/env python
# encoding: utf-8

from ecollector import models
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://ecollector:password'
                       '@localhost/ecollector', pool_recycle=3600)

models.metadata.create_all(engine)
