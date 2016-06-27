# -*- coding: UTF-8 -*-
__author__ = 'Jeffrey'

import time
import traceback
import functools








def logging(*args):
    print args

def error_catch(func):
    functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logging("error", e, traceback.format_exc())
    return wrapper



@error_catch
def printer():
    print str()+1


if __name__ == "__main__":
    pass