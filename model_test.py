# -*- coding: UTF-8 -*-
__author__ = 'Jeffrey'


from DBManager import QDB
from models import Model, IntegerField, JsonDictField,StringField


class UserModel(Model):
    __db_table = "user"

    sex = StringField(default="no", max_length=10)
    nickName = StringField(default="no", max_length=10)
    pk = IntegerField(default=45)
    data = JsonDictField(default={1:2})

    def __init__(self):
        super(UserModel, self).__init__(self)


if __name__ == "__main__":
    uM = UserModel.field('id', 'nickName', 'sex').filter(id=7).results()[0]
    print uM.id, uM.nickName, uM.sex

