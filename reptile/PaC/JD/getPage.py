# encoding:utf-8

 

import bs4
import requests
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

import os
import time
import json
import random
import argparse
import sys
import importlib

importlib.reload(sys)
 

class JDWrapper(object):
    '''
    This class used to simulate login JD
    '''

    def __init__(self, usr_name=None, usr_pwd=None):
        # cookie info
        self.trackid = ''
        self.uuid = ''
        self.eid = ''
        self.fp = '' 
        self.interval = 0

        # init url related 
        # requests.Session()会话对象能够实现跨请求保持某些参数。它也会在同一个 Session 实例发出的所有请求之间保持 cookie
        self.sess = requests.Session()
        self.sess.trust_env = False
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'ContentType': 'text/html; charset=utf-8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
        }

        self.cookies = {

        }
 


    def getPage(self):
        # jd login by QR code
         
        # 我的购物车页面:
        # http://m.17u.cn/client/dj/[refid]
        #
        stock_link = 'http://m.17u.cn/app/pje/[refid]?sUrl=shouji.17u.cn|internal|h5|file|3|main.html?wvc1=1&wvc2=1&wvc3=1#|detail|89143|0|%5E7006%5E89143%5E&rUrl=http://m.ly.com/dujia/tours/69676.html'
        resp = self.sess.get(stock_link)
        soup = bs4.BeautifulSoup(resp.text, "html.parser")
        f = open(os.path.join(os.getcwd(), "getPage.txt")  , 'a+')
        f.writelines( soup.prettify())
        f.close()






def main(options):
    #
    jd = JDWrapper()

    jd.getPage()




if __name__ == '__main__':

    # get_cur_info()

    parser = argparse.ArgumentParser(description='Simulate to login Jing Dong, and buy sepecified good')


    options = parser.parse_args()
    print (options)

    main(options)

