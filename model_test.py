# -*- coding: UTF-8 -*-
__author__ = 'Jeffrey'


from DBManager import QDB
from models import Model, IntegerField, JsonDictField


class UserModel(Model):
    __db_table = "user"

    pk = IntegerField(default=45)
    data = JsonDictField(default={1:2})

class Test(object):



    @staticmethod
    def test(func):
        def wrapper(*args):
            func(args)
            if args[0]!= 0:
                return "1"
            else:
                return "0"
        return wrapper

@Test.test
def tt1(a):
    pass



if __name__ == "__main__":
    uM = UserModel.get(id=1).results()
