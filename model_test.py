# -*- coding: UTF-8 -*-
__author__ = 'Jeffrey'


from DBManager import QDB
from models import Model, IntegerField, JsonDictField


class UserModel(Model):
    __db_table = "user"

    pk = IntegerField(default=45)
    data = JsonDictField(default={1:2})


if __name__ == "__main__":
    uM = UserModel.field('id', 'nickname').get(id=1).results()
    print(uM.id)
