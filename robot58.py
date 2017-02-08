# -*- coding: utf-8 -*-
'''
author: fuxy
'''
import datetime
import time
import requests
import traceback
import re
import json


class Robot_58(object):
    cookie_path_58 = r"/var/moji/log/cookie_58.txt"
    sum_jsonp = "&callback=jQuery18308715175740344805_1486360265758&_="
    channel_jsonp = "&callback=jQuery183029710456491913484_1486354133961&_="

    channel_58_url = "http://union.58.com/api/icdata?media_name=%E5%A2%A8%E8%BF%B9%E5%A4%A9%E6%B0%94&channel=D.C.D&"
    sum_58_url = "http://union.58.com/api/icdata?media_name=&channel=&"

    headers_58 = {
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'union.58.com',
        'Pragma': 'no-cache',
        'Referer': 'http://union.58.com/detail',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    def __init__(self, timestamp=None):
        if timestamp:
            self.begin_time = timestamp
            self.end_time = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            self.begin_time = self.end_time = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        self.requests_time_stamp = int(time.time() * 1000)

        self.channel_58_url = self.channel_58_url + ("start=%s&end=%s" % (self.begin_time, self.end_time)) + self.channel_jsonp + str(self.requests_time_stamp)
        self.sum_58_url = self.sum_58_url + ("start=%s&end=%s" % (self.begin_time, self.end_time)) + self.sum_jsonp +  str(self.requests_time_stamp)

        self.conn_58 = requests.Session()
        self.conn_58.headers.update(self.headers_58)
        self.cookies_58 = self.load_cookie(self.cookie_path_58)

    def get_58_sum_data(self):
        try:
            r = self.conn_58.get(self.sum_58_url, cookies=self.cookies_58)
            self.cookies_58 = self.parse_cookie(r.request.headers['Cookie'])
            self.store_cookie(r.request.headers['Cookie'], self.cookie_path_58)
            return self.parse_jsonp(r.text)
        except:
            traceback.print_exc()
            return ''

    def get_58_channel_data(self):
        try:
            r = self.conn_58.get(self.channel_58_url, cookies=self.cookies_58)
            self.cookies_58 = self.parse_cookie(r.request.headers['Cookie'])
            self.store_cookie(r.request.headers['Cookie'], self.cookie_path_58)
            return self.parse_jsonp(r.text)
        except:
            traceback.print_exc()
            return ''

    def parse_cookie(self, str):
        cookies={}
        for line in str.split(';'):  
            key,value=line.strip().split('=',1)
            cookies[key]=value
        return cookies

    def load_cookie(self, path):
        cookies={}
        with open(path) as f:
            str = f.read()
            for line in str.split(';'):  
                key,value=line.strip().split('=',1)
                cookies[key]=value
        return cookies

    def store_cookie(self, str, path):
        with open(path, "wb") as f:
            f.write(str)
            f.close()

    def parse(self):
        print '---58---'
        print self.get_58_sum_data()
        print self.get_58_channel_data()

    def parse_jsonp(self, str):
        return json.loads(re.match(".*?({.*}).*", str, re.S).group(1))["content"]


def run():
    print datetime.datetime.now()
    try:
        Robot_58().parse()
    except:
        traceback.print_exc()


if __name__ == '__main__':
    run()


