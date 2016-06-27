# -*- coding: UTF-8 -*-
__author__ = 'Jeffrey'

import traceback
import json

from DBManager import QDB
from utils import logging

class ModelMetaClass(type):
    def __new__(mcs, name, base_tuple, attr_dict):

        return super(ModelMetaClass, mcs).__new__(mcs, name, base_tuple, attr_dict)


class IntegerField(object):
    def __new__(cls, default=0, help_text="", *args, **kwargs):

        try:
            number = int(default)
            return number
        except Exception as e:
            logging("error", e, traceback.format_exc())
            return 0

class StringField(object):
    def __new__(cls, default="", max_length=0, help_text="", *args, **kwargs):
        if len(default) > max_length:
            logging("error","已超过最大长度!")
        else:
            return default

class TextField(object):
    pass

class JsonDictField(object):
    def __new__(cls, default={}, *args, **kwargs):
        try:
            if isinstance(default, dict):
                cls._data =default
                return super(JsonDictField, cls).__new__(cls,*args, **kwargs)
                #return cls
            logging("error", u"默认参数不是字典!")
            return {}
        except Exception as e:
            logging("error", e, traceback.format_exc())
            return {}


    def __str__(self):
        return json.dumps(self._data)

    def save_into_db(self):
        pass

class JsonListField(object):
    def __new__(cls, default={}, *args, **kwargs):
        try:
            if isinstance(default, list):
                cls._data =default
                return super(JsonListField, cls).__new__(cls,*args, **kwargs)
                #return cls
            logging("error", u"默认参数不是列表!")
            return {}
        except Exception as e:
            logging("error", e, traceback.format_exc())
            return {}


    def __str__(self):
        return json.dumps(self._data)

    def save_into_db(self):
        pass



class SqlCreator(object):

    __index = 0

    __where_text = ""
    __field_text = ""
    __reverse_text = ""
    __order_by = ""


    @QDB.execute_sql
    def where(self, **kwargs):
        self.__where_text = " and ".join([k + "="+ str(v) for k,v in kwargs.items()])
        print self.__index
        return self

    def field(self, *args):
        self.__field_text = ','.join(args) if args else ""
        return self

    def reverse(self, isReverse):
        self.__reverse_text = 'DESC' if isReverse else "ASC"
        return self

    def order_by(self,*args):
        self.__order_by = "order by" + ",".join(args) if args else ""
        return self

    def execute_sql(self, db):
        pass



class Model(object):
    _attr_dict = {}
    _connect = None
    _db = None
    _result = None

    objects = SqlCreator()
    def __new__(cls):
        return super(Model, cls).__new__(cls, cls.__name__, (object,), cls._attr_dict)

    def __init__(self, *args, **kwargs): # 用于创建
        self._table = self.__getattribute__(''.join(["_",self.__class__.__name__, "__db_table"]))
        self._connect = QDB.connector
        self._db = self._connect.cursor()
        # self._objects = SqlCreator()
        super(Model, self).__init__(self, *args, **kwargs)


    def close(self):
        if self._db:
            self._db.close()
        if self._connect:
            self._connect.close()

    def get(self, **kwargs):
        _where = (''.join([k + "="+ str(v)+" and " for k,v in kwargs.items()]))[:-4] # 去掉最后一个and
        _sql = "select * from %s where " % (self._table,) +  _where
        self._db.execute(_sql)
        self._result = self._db.fetchone()
        self.close()
        return self

    def __getattribute__(self, item):
        if item in dir(self):
            print self.get('item')













