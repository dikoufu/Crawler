# -*- coding: utf-8 -*-
'''
author: fuxy
'''
import datetime
import time
import requests
import traceback


class Robot_baidu(object):
    baidu_cookie_path = r"/var/moji/log/baidu_cookie.txt"
    first_request = 1
    baidu_sum_url = "http://mssp.baidu.com/app/api/js/reports?timeGranularity=day&metrics=view%2Cclick%2CfillRatio%2CclickRatio%2Cecpm%2Ccpc%2Cincome"
    # app_url = "http://mssp.baidu.com/app/api/js/reports?timeGranularity=sum&metrics=view%2Cclick%2CfillRatio%2CclickRatio%2Cecpm%2Ccpc%2Cincome&pageNo=1&order=desc&orderBy=appName&dimensions=appId%2CappName%2CsystemId%2CsystemName&pageSize=50"
    baidu_code_url = "http://mssp.baidu.com/app/api/js/reports?timeGranularity=sum&metrics=view%2Cclick%2CfillRatio%2CclickRatio%2Cecpm%2Ccpc%2Cincome&pageNo=1&order=desc&orderBy=adPositionName&dimensions=adPositionId%2CadPositionName%2CadTypeId%2CadTypeName&pageSize=100"

    baidu_sum_ref = "http://mssp.baidu.com/app/static/main.html/report/total~begin=%s&end=%s"
    # app_ref = "http://mssp.baidu.com/app/static/main.html/report/app"
    baidu_code_ref = "http://mssp.baidu.com/app/static/main.html/report/adPosition"

    baidu_header = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Host':'mssp.baidu.com',
        'Pragma':'no-cache',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }

    def __init__(self, timestamp=None):
        if timestamp:
            self.begin_time = timestamp
            self.end_time = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
        else:
            self.begin_time = self.end_time = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
        
        self.baidu_sum_url = self.baidu_sum_url + ("&begin=%s&end=%s" % (self.begin_time, self.end_time))
        self.baidu_sum_ref = self.baidu_sum_ref % (self.begin_time, self.end_time)

        self.baidu_code_url = self.baidu_code_url + ("&begin=%s&end=%s" % (self.begin_time, self.end_time))

        self.baidu_conn = requests.Session()
        self.baidu_conn.headers.update(self.baidu_header)
        self.baidu_cookies = self.load_cookie(self.baidu_cookie_path)

    def get_baidu_sum_data(self):
        self.baidu_conn.headers.update({'Referer': self.baidu_sum_ref})
        try:
            r = self.baidu_conn.get(self.baidu_sum_url, cookies=self.baidu_cookies)
            sum_data = r.json()
            self.baidu_cookies = self.parse_cookie(r.request.headers['Cookie'])
            self.store_cookie(r.request.headers['Cookie'], self.baidu_cookie_path)
            return sum_data['results']
        except:
	    traceback.print_exc()
            return ""

    # def get_app_data(session, begin_time, end_time):
    #    session.headers.update({'Referer': app_ref})
    #    app_url_ = app_url + ("&begin=%s&end=%s" % (begin_time, end_time))
    #    r = session.get(app_url_)
    #    app_data = r.json()
    #    print app_data['results']

    def get_baidu_code_data(self):
        self.baidu_conn.headers.update({'Referer': self.baidu_code_ref})
        try:
            r = self.baidu_conn.get(self.baidu_code_url, cookies=self.baidu_cookies)
            app_data = r.json()
            self.baidu_cookies = self.parse_cookie(r.request.headers['Cookie'])
            self.store_cookie(r.request.headers['Cookie'], self.baidu_cookie_path)
            return app_data['results']
        except:
            traceback.print_exc()
            return ""

    # input: raw cookie
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
        print '---baidu---'
        print self.get_baidu_sum_data()
        print self.get_baidu_code_data()


def run():
    print datetime.datetime.now()
    try:
        Robot_baidu().parse()
    except:
        traceback.print_exc()


if __name__ == '__main__':
    run()

