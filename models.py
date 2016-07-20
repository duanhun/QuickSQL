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







class Model(object):
    _attr_dict = {}
    _connect = None
    _db = None
    _result = None

    __index = 0

    __sql = ""
    __option = ""
    __where_text = ""
    __field_text = ""
    __fields = []
    __reverse_text = ""
    __order_by = ""

    def __new__(cls):
        return super(Model, cls).__new__(cls, cls.__name__, (object,), cls._attr_dict)

    @classmethod
    def __getattribute__(self, item):
        if item in dir(self):
            return getattr(self,item)
        else:
            return None

    def __init__(self, *args, **kwargs): # 用于创建某个实例
        # self._objects = SqlCreator()
        super(Model, self).__init__(self, *args, **kwargs)

    @classmethod
    def close(self):
        if self._db:
            self._db.close()
        if self._connect:
            self._connect.close()

    @classmethod
    def get(cls, **kwargs):
        cls.__option = "select"
        return cls.filter(**kwargs)

    @classmethod
    def update(cls, **kwargs):
        cls.__option = "update"
        return cls.filter(**kwargs)

    @classmethod
    def filter(cls, **kwargs):
        cls.__where_text += " and ".join([k + "="+ str(v) for k,v in kwargs.items()])
        return cls

    @classmethod
    def field(cls, *args):
        cls.__fields = args
        cls.__field_text += ','.join(args) if args else ""
        return cls

    @classmethod
    def reverse(cls, isReverse):
        cls.__reverse_text += 'DESC' if isReverse else "ASC"
        return cls

    @classmethod
    def order_by(cls,*args):
        cls.__order_by = ("order by" + ",".join(args)) if args else ""
        return cls



    @classmethod
    def results(cls):
        cls._connect = QDB.connector
        cls._db = cls._connect.cursor()
        cls.__sql = ""
        cls._table = cls.__getattribute__(''.join(["_", cls.__name__, "__db_table"]))
        if cls.__option == "select":
            cls.__sql = cls.__option + " " + (cls.__field_text if cls.__field_text else "*") + \
                        " from "+ str(cls._table) + " where " + cls.__where_text + " " + cls.__order_by + cls.__reverse_text


        result = cls._db.execute(cls.__sql)
        model = cls._db.fetchone()
        print cls.__sql
        cls.__model = {}
        for field, data in zip(cls.__fields, model):
            setattr(cls, field, data)
        cls.close()

        cls.__sql = ""
        return cls














