# -*- coding: utf-8 -*-
'''
author: fuxy
'''
from crawler import Robot_baidu
from robot58 import Robot_58
import traceback
import time
import datetime


if __name__ == '__main__':
    while 1:
        try:
            print datetime.datetime.now()
            Robot_baidu().parse()
            Robot_58().parse()
        except:
            traceback.print_exc()
        time.sleep(50)
