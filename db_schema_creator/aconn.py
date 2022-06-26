# -*- coding: utf-8 -*-

import os
import datetime
import sys

os.environ["PATH"] = "C:\oracle\instantclient_12_2;" + os.environ["PATH"]

# import cx_Oracle

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Query
from sqlalchemy.engine import Engine
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.engine import ResultProxy


class AConnector:
    def status(self, text=None):
        if text is None:
            print("\r                                                                                   \r", end="")
            sys.stdout.flush()
        else:
            print("\r{0}> {1}                                                                                 ".format(
                datetime.datetime.now().strftime("%H:%M:%S"), text), end="")
            sys.stdout.flush()

    def log(self, text):
        if self.logger_fnc is None:
            print('[%s] %s                                             ' % (self.name, text))
        else:
            self.logger_fnc(text)


    def __init__(self, db_name, conn_str, schema_name='maximo', logger_fnc=None, **kwargs):
        self.logger_fnc = logger_fnc
        self.schema = schema_name
        self.name = str(db_name).lower()

        self.engine = create_engine(conn_str, **kwargs)   # type: Engine
        self.engine.connect()
        # self.log('Connection created')
        self.meta = MetaData()
        self.inspector = Inspector.from_engine(self.engine)  # type: Inspector
        # self.log('Inspector done')
        self.Session = sessionmaker()  # type: orm.Session
        self.Session.configure(bind=self.engine)
        self.con = self.Session()  # type: orm.Session
        self.log('Connected to %s' % conn_str)

    def query(self, *args, **kwargs) -> Query:
        return self.con.query(*args, **kwargs)

    def sql(self, *args, **kwargs) -> ResultProxy:
        return self.engine.execute(*args, **kwargs)
