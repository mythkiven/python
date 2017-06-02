# encoding:utf-8


"""

 JD 登录

"""


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


"""
1. 函数: Python提供许多内建函数,例如: print()
自定义函数:
def 函数名（参数列表）:
    函数体

2. 变量类型:
在 python 中，类型属于对象，变量是没有类型的：
a=[1,2,3]
a="Runoob"
以上代码中，[1,2,3] 是 List 类型，"Runoob" 是 String 类型，而变量 a 是没有类型.
她仅仅是一个对象的引用（一个指针），可以是 List 类型对象，也可以指向 String 类型对象。
3. 可变(mutable)与不可变(immutable)对象
在 python 中，strings, tuples, 和 numbers 是不可变对象(如a = "ss" fun（a）将 a副本传到函数)，而 list,dict 等则是可以修改的对象(变量赋值 la=[1,2,3,4] fun(la),将 la对象/指针传进去)。
4.匿名函数: lambda [arg1 [,arg2,.....argn]]:expression
例如: sum = lambda arg1, arg2: arg1 + arg2;
print ("相加后的值为 : ", sum( 10, 20 ))


 知识点1:
python 使用 lambda 来创建匿名函数(匿名: 不使用 def 标准的形式定义函数)
案例:
sum = lambda arg1, arg2: arg1 + arg2;
print ("相加后的值为 : ", sum( 10, 20 ))
说明:
lambda 只是一个表达式，函数体比 def 简单很多。
lambda 的主体是一个表达式，而不是一个代码块。仅仅能在lambda表达式中封装有限的逻辑进去。
lambda 函数拥有自己的命名空间，且不能访问自有参数列表之外或全局命名空间里的参数。
lambda 函数看起来只能写一行，却不等同于C或C++的内联函数，后者的目的是调用小函数时不占用栈内存从而增加运行效率。

本例: FuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name
FuncName 函数用于

try:
    .....
except (Exception) as e:
    print ('Exp {0} : {1}'.format(FuncName(), e))

    首先，执行try子句（在关键字try和关键字except之间的语句）
如果没有异常发生，忽略except子句，try子句执行后结束。
如果在执行try子句的过程中发生了异常，那么try子句余下的部分将被忽略。如果异常的类型和 except 之后的名称相符，那么对应的except子句将被执行。最后执行 try 语句之后的代码。
如果一个异常没有与任何的except匹配，那么这个异常将会传递给上层的try中。

解释:
    传入:FuncName(x),x不传,使用默认值 n=0.
    sys._getframe().f_code.co_filename  #当前文件名，可以通过__file__获得
    sys._getframe(0).f_code.co_name  #当前函数名
    sys._getframe(1).f_code.co_name　#调用该函数的函数的名字，如果没有被调用，则返回<module>，貌似call stack的栈低
    sys._getframe().f_lineno #当前行号

"""


# def get_cur_info():
#     print ('当前路径文件名:', sys._getframe().f_code.co_filename, "哈哈")
#     print ('当前函数名:', sys._getframe(0).f_code.co_name)
#     print ('调用函数名,没调用 module:', sys._getframe(1).f_code.co_name)
#     print ('当前行号:', sys._getframe().f_lineno)
#
#
# # #打印函数名以及是否调用:
# FuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name
#
#
# def tags_val(tag, key='', index=0):
#     '''
#     return html tag list attribute @key @index
#     if @key is empty, return tag content
#     '''
#     if len(tag) == 0 or len(tag) <= index:
#         return ''
#     elif key:
#         txt = tag[index].get(key)
#         # strip(aa) 方法用于移除字符串头尾指定的字符aa（默认为空格）
#         return txt.strip(' \t\r\n') if txt else ''
#     else:
#         txt = tag[index].text
#         return txt.strip(' \t\r\n') if txt else ''
#
#
# def tag_val(tag, key=''):
#     '''
#     return html tag attribute @key
#     if @key is empty, return tag content
#     '''
#     if tag is None:
#         return ''
#     elif key:
#         txt = tag.get(key)
#         return txt.strip(' \t\r\n') if txt else ''
#     else:
#         txt = tag.text
#         return txt.strip(' \t\r\n') if txt else ''


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

        self.usr_name = usr_name
        self.usr_pwd = usr_pwd

        self.interval = 0

        # init url related
        self.home = 'https://passport.jd.com/new/login.aspx'
        self.login = 'https://passport.jd.com/uc/loginService'
        self.imag = 'https://authcode.jd.com/verify/image'
        self.auth = 'https://passport.jd.com/uc/showAuthCode'
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

        '''
        try:
            self.browser = webdriver.PhantomJS('phantomjs.exe')
        except Exception, e:
            print 'Phantomjs initialize failed :', e
            exit(1)
        '''


    def login_by_QR(self):
        # jd login by QR code
        try:
            print ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print (u'{0} > 请打开京东手机客户端，准备扫码登陆:'.format(time.ctime()))

            urls = (
                'https://passport.jd.com/new/login.aspx',
                'https://qr.m.jd.com/show',
                'https://qr.m.jd.com/check',
                'https://passport.jd.com/uc/qrCodeTicketValidation'
            )

            # step 1: open login page
            resp = self.sess.get(
                urls[0],
                headers=self.headers
            )
            if resp.status_code != requests.codes.OK:
                print (u'获取登录页失败: %u' % resp.status_code)
                return False

            ## save cookies
            for k, v in resp.cookies.items():
                self.cookies[k] = v

            # step 2: get QR image
            resp = self.sess.get(
                urls[1],
                headers=self.headers,
                cookies=self.cookies,
                params={
                    'appid': 133,
                    'size': 147,
                    't': (int)(time.time() * 1000)
                }
            )
            if resp.status_code != requests.codes.OK:
                print (u'获取二维码失败: %u' % resp.status_code)
                return False

            ## save cookies
            for k, v in resp.cookies.items():
                self.cookies[k] = v

            ## save QR code
            image_file = 'qr.png'
            with open(image_file, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=1024):
                    f.write(chunk)

            ## scan QR code with phone
            os.system('start ' + image_file)

            # step 3： check scan result
            ## mush have
            self.headers['Host'] = 'qr.m.jd.com'
            self.headers['Referer'] = 'https://passport.jd.com/new/login.aspx'

            # check if QR code scanned
            qr_ticket = None
            retry_times = 100
            while retry_times:
                retry_times -= 1
                resp = self.sess.get(
                    urls[2],
                    headers=self.headers,
                    cookies=self.cookies,
                    params={
                        'callback': 'jQuery%u' % random.randint(100000, 999999),
                        'appid': 133,
                        'token': self.cookies['wlfstk_smdl'],
                        '_': (int)(time.time() * 1000)
                    }
                )

                if resp.status_code != requests.codes.OK:
                    continue

                n1 = resp.text.find('(')
                n2 = resp.text.find(')')
                rs = json.loads(resp.text[n1 + 1:n2])

                if rs['code'] == 200:
                    print (u'{} : {}'.format(rs['code'], rs['ticket']))
                    qr_ticket = rs['ticket']
                    break
                else:
                    print (u'{} : {}'.format(rs['code'], rs['msg']))
                    time.sleep(3)

            if not qr_ticket:
                print (u'二维码登陆失败')
                return False

            # step 4: validate scan result
            ## must have
            self.headers['Host'] = 'passport.jd.com'
            self.headers['Referer'] = 'https://passport.jd.com/uc/login?ltype=logout'
            resp = self.sess.get(
                urls[3],
                headers=self.headers,
                cookies=self.cookies,
                params={'t': qr_ticket},
            )
            if resp.status_code != requests.codes.OK:
                print (u'二维码登陆校验失败: %u' % resp.status_code)
                return False

            ## login succeed
            self.headers['P3P'] = resp.headers.get('P3P')
            for k, v in resp.cookies.items():
                self.cookies[k] = v

            print (u'登陆成功')
            return True

        except Exception as e:
            print ('Exp:', e)
            raise

        return False



    def getPage(self):
        print ('登录成功, 获取对应的web页面')
        # 登录成功, 获取对应的web页面


        # 我的购物车页面:
        stock_link = 'https://cart.jd.com/cart.action'
        resp = self.sess.get(stock_link)
        soup = bs4.BeautifulSoup(resp.text, "html.parser")
        f = open(os.path.join(os.getcwd(), "我的购物车页面.txt")  , 'a+')
        f.writelines( soup.prettify())
        f.close()


        # 我的关注页面:
        stock_link2 = 'https://t.jd.com/home/follow'
        resp2 = self.sess.get(stock_link2)
        soup2 = bs4.BeautifulSoup(resp2.text, "html.parser")
        f = open(os.path.join(os.getcwd(), "关注页面.txt"), 'a+')
        f.writelines(soup.prettify())
        f.close()

        # 我的订单页面:
        stock_link3 = 'https://order.jd.com/center/list.action?search=0&d=2&s=4096'
        resp3 = self.sess.get(stock_link3)
        soup3 = bs4.BeautifulSoup(resp3.text, "html.parser")
        f = open(os.path.join(os.getcwd(), "订单页面.txt"), 'a+')
        f.writelines(soup.prettify())
        f.close()

        # # 我的金库页面:
        # stock_link4 = 'https://jinku.jd.com/xjk/income.action'
        # resp4 = self.sess.get(stock_link4)
        # soup4 = bs4.BeautifulSoup(resp4.text, "html.parser")
        # print ('我的金库页面::', soup4)
        #
        # f = open(os.path.join(os.getcwd(), "我的购物车页面.txt"), 'a+')
        # f.writelines(soup.prettify())
        # f.close()
        #
        #
        # # 我的JD资产页面:
        # stock_link3 = 'https://jinku.jd.com/xjk/income.action'
        # resp3 = self.sess.get(stock_link3)
        # soup3 = bs4.BeautifulSoup(resp3.text, "html.parser")
        # print ('我的JD 资产页面::', soup3)
        #
        # f = open(os.path.join(os.getcwd(), "我的购物车页面.txt"), 'a+')
        # f.writelines(soup.prettify())
        # f.close()
        #
        # # 我的JD白条页面:
        # stock_link3 = 'https://jinku.jd.com/xjk/income.action'
        # resp3 = self.sess.get(stock_link3)
        # soup3 = bs4.BeautifulSoup(resp3.text, "html.parser")
        # print ('我的JD白条页面::', soup3)
        #
        # f = open(os.path.join(os.getcwd(), "我的购物车页面.txt"), 'a+')
        # f.writelines(soup.prettify())
        # f.close()
#
# """
# 代码中经常会有变量是否为None的判断，有三种主要的写法：
#  第一种是`if x is None`；
# 第二种是 `if not x：`；
# 第三种是`if not x is None`（这句这样理解更清晰`if not (x is None)`）
# 结论：
# `if x is not None`是最好的写法，清晰，不会出现错误，以后坚持使用这种写法。
# 使用if not x这种写法的前提是：必须清楚x等于None,  False, 空字符串"", 0, 空列表[], 空字典{}, 空元组()时对你的判断没有影响才行。
#
#
# while not jd.buy(options) and options.flush:
#  ----not jd.buy(options) 为真---- options.flush为真,则执行后边的语句
# """
#
#
#




def main(options):
    #
    jd = JDWrapper()
    if not jd.login_by_QR():
        return

    jd.getPage()




if __name__ == '__main__':

    # get_cur_info()

    parser = argparse.ArgumentParser(description='Simulate to login Jing Dong, and buy sepecified good')


    options = parser.parse_args()
    print (options)

    main(options)

