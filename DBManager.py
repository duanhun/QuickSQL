# -*- coding: UTF-8 -*-
__author__ = 'Jeffrey'

import MySQLdb

from utils import error_catch, logging

class Connector(object):
    _index = 0

    @error_catch
    def __init__(self, host, user, pwd, dbName, port=3306, charset="utf8"):

        self._host = host
        self._user = user
        self._pwd = pwd
        self._dbName = dbName
        self._port = port
        self._charset = charset
        self._connector = MySQLdb.connect(host=self._host, user=self._user, passwd=self._pwd, db=self._dbName, port=self._port, charset=self._charset)

    @property
    def connector(self):
        return self._connector

    @connector.setter
    def connector(self, connector=None):
        if not connector:
            raise
        self._connector = connector

    def close(self):
        self._connector.cursor().close()
        self._connector.close()
        logging("error", "DBM close!")

    @classmethod
    def execute_sql(cls,func):

        def wrapper(*args,**kwargs):
            print func.__class__, func.__name__
            return func(*args,**kwargs)

        return wrapper

QDB = Connector("localhost", "root", "123456", "youaiwang", 3306)