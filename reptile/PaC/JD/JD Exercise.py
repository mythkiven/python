# encoding:utf-8


# 导入模块:

import requests #网络模块
import os   #系统模块
import time # 日期模块
import json # json 解析
import random #随机数模块

import bs4 # 解析网页

#定义JD类 扫码登录类:

class JDLoginByQR():

#初始化
    def __init__(self):

        self.request = requests.Session()

        # 处理SSL,代理错误: Caused by ProxyError('Cannot connect to proxy.'
        # trust_env:取用系統環境變數 =False，將忽略以下系統參數:系統的 proxys/.netrc 的身份認證/定義在 REQUESTS_CA_BUNDLE 中的 CA bundles CURL_CA_BUNDLE
        self.request.trust_env = False
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'ContentType': 'text/html; charset=utf-8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
        }
        self.cookies = {

        }

#自定义方法
    def login_by_QR(self):
        #调用方法后会不断的轮训状态,所以要使用 try:方法
        try:
            print('++++++++++++++++++++++++++++++++++++++++++++++++')
            print(u'{0} >> 请打开 JD 手机客户端,准备扫码登录.'.format(time.time()))
            urls = (
                'https://passport.jd.com/new/login.aspx',
                'https://qr.m.jd.com/show',
                'https://qr.m.jd.com/check',
                'https://passport.jd.com/uc/qrCodeTicketValidation' #这个是校验登录的
            )

            # 1. 获取登录页面:
            resp = self.request.get(
                urls[0],
                headers=self.headers
            )
            ''' resp 关键点:
            text: 内容
            cookies:\headers:\status_code:状态码
            '''
            if resp.status_code != requests.codes.OK:
                print(u'获取登录页面失败,状态码:%u',resp.status_code)
                return False
            # 1.1 填充 cookie
            for k,v in resp.cookies.items():
                self.cookies[k]=v

            # 2. 获取二维码图片
            resp = self.request.get(
                urls[1],
                headers=self.headers,
                cookies=self.cookies,
                params={
                    'appid':133,
                    'size':147,
                    't':(int)(time.time()*1000)
                }
            )
            if resp.status_code != requests.codes.OK:
                print(u'获取二维码失败:%u',resp.status_code)
                return False
            # 2.1 保存 cookie
            for k,v in resp.cookies.items():
                self.cookies[k]=v
            # 2.2 保存二维码图片
            image_file = 'qr_test.png'
            with open(image_file,'wb') as f:
                for chunk in resp.iter_content(chunk_size=1024):
                    f.write(chunk)

            # 接下来就要不断的轮训扫码状态了.

            # 3
            retry_times = 100
            qr_ticket = None
            # 注意,这里设置Referer的原因,参见下边解说, 最初不设置会报错,参数不对, 看看 charles就明白,缺了这东西.
            self.headers['Referer']='https://passport.jd.com/uc/login?ltype=logout'
            while retry_times:
                retry_times -= 1
                resp = self.request.get(
                    urls[2],
                    headers=self.headers,
                    cookies=self.cookies,
                    params={
                        'callback':'jQuery%u' % random.randint(100000,999999),
                        'appid':133,
                        'token':self.cookies['wlfstk_smdl'], # token 可以在 charles中查询,找到对应的 key
                        '_':(int)(time.time()*1000)
                    }
                )

                if resp.status_code != requests.codes.OK:
                    continue
                '''
                这样直接操作,报错, 看看 Charles:明白了, 需要添加 referer: https://passport.jd.com/uc/login?ltype=logout
                在 headers中
                '''
                #print('扫码状态:'+resp.text)

                # 获取 json 串
                n1=resp.text.find('(')
                n2=resp.text.find(')')
                rs=json.loads(resp.text[n1+1:n2])
                if rs['code'] == 200:
                    # 保存 cookie:
                    for k, v in resp.cookies.items():
                        self.cookies[k] = v
                    qr_ticket=rs['ticket']
                    print(u'成功状态码:{} ticket:{}'.format(rs['code'],rs['ticket']))
                    break # break 表示继续执行后边的代码,但是终止掉 while. 使用 continue则是继续执行代码, 不会终止掉 while.还是会再次执行 while
                else:
                    print(u'状态码:{} 消息:{}'.format(rs['code'],rs['msg']))
                    #等会再轮训一次, 否则会太快了...
                    time.sleep(3)
            if not qr_ticket:
                print (u'二维码登陆失败')
                return False
            '''
            下边是第二步:校验取登录的状态,其中设置都是来自 charles.
            '''
            self.headers['Host'] = 'passport.jd.com'
            self.headers['Referer'] = 'https://passport.jd.com/uc/login?ltype=logout'
            resp = self.request.get(
                urls[3],
                headers=self.headers,
                cookies=self.cookies,
                params={'t':qr_ticket},
             )
            if resp.status_code != requests.codes.OK:
                print (u'二维码登录校验失败:%u'%resp.status_code)
                return  False
            for k,v in resp.cookies.items():
                self.cookies[k]=v

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
        resp = self.request.get(
            stock_link)
        soup = bs4.BeautifulSoup(resp.text, "html.parser")
        f = open(os.path.join(os.getcwd(), "我的购物车页面.txt"), 'a+')
        f.writelines(soup.prettify())
        f.close()

        # 我的关注页面:
        stock_link2 = 'https://t.jd.com/home/follow'
        resp2 = self.request.get(
            stock_link2,)
        soup2 = bs4.BeautifulSoup(resp2.text, "html.parser")
        f = open(os.path.join(os.getcwd(), "关注页面.txt"), 'a+')
        f.writelines(soup.prettify())
        f.close()

        # 我的订单页面:
        stock_link3 = 'https://order.jd.com/center/list.action?search=0&d=2&s=4096'
        resp3 = self.request.get(
            stock_link3)
        soup3 = bs4.BeautifulSoup(resp3.text, "html.parser")
        f = open(os.path.join(os.getcwd(), "订单页面.txt"), 'a+')
        f.writelines(soup.prettify())
        f.close()



def main():
    #
    jd = JDLoginByQR()
    if not jd.login_by_QR():
        return

    jd.getPage()

if __name__ == '__main__':

    main()















