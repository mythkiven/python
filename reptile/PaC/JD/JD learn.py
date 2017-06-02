#encoding:utf-8

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

'''
Python 日期和时间:
    每个时间戳都以自从1970年1月1日午夜（历元）经过了多长时间来表示
    time.time(): 获取当前时间戳:  1459994552.51
    time.ctime(): 输出本地时间 :  Thu May 25 09:58:06 2017
    int(time.time() * 1000) 当前时间的毫秒表示
JD 登录的 URL: https://passport.jd.com/new/login.aspx?ReturnUrl=https://trade.jr.jd.com/centre/browse.action

'''

''' -------- 博客的登录: 关于:登录URL的格式问题 xxx/login.aspx?ReturnUrl=xxxx -----
案例解说:
    登陆URL: kkloginurl == https://passport.cnblogs.com/user/signin
    博客页面: (kkurl == http://www.cnblogs.com/xiexj/p/6897806.html) 点击关注博主.
情形1: 点击关注博主, 会进入登录页面, 登录后还要返回 A 页面:
    此时的登录页面是: kkloginurl?ReturnUrl=http://www.cnblogs.com/xiexj/p/6897806.html#undefined.
    当登录成功之后, 就会重新跳转到:kkurl

情形2: 点击关注, 跳入登录, 登录之后, 进入主页:
    此时的登录页面是:  kkloginurl

看看登录页面的源码:
------情况1:
登录页面URL:https://passport.cnblogs.com/user/signin?ReturnUrl=http://www.cnblogs.com/xiexj/p/6897806.html#undefined.
    <script>
        var return_url = 'http://www.cnblogs.com/xiexj/p/6897806.html#undefined#undefined';
        ....
        $.ajax({
                url: ajax_url,   type: 'post',   data: JSON.stringify(ajax_data),  contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                headers: { 'VerificationToken': 'lz8xctoGu1jylqP0f-WuKGNn11JjWAArDEhI2S4J13U8OeuR7f5J1i7u_oanv2qZKuZLp1zbz6NpvbFD7JBMxDiVwLg1:2yKdmOOYc5yhgKody27kqNCrGpU9wS_5VykvqMYbl85CF5mWoY6xHY1F-CzdXuZkTe_FTfH9-bQfdLZG9CJSJdlfJ2g1'
                },
                success: function (data) {
                    if (data.success) {
                        $('#tip_btn').html('登录成功，正在重定向...');
                        location.href = return_url;  <<<<这里登录成功了,会重定向>>>>
                    } else {
                        $('#tip_btn').html(data.message + "<br/><br/>联系 contact@cnblogs.com");
                        is_in_progress = false;
                        if(enable_captcha) {  captchaObj.ReloadImage();  }
                    }
                },
                error: function (xhr) {
                    is_in_progress = false;
                    $('#tip_btn').html('抱歉！出错！联系 contact@cnblogs.com');
                }
            });
        ....
------情况2: 登录页面逻辑, 重定向到首页
登录页面URL:https://passport.cnblogs.com/user/signin
    <script>
        var return_url = 'http://home.cnblogs.com';
        $.ajax({ <<<<<<同上>>>> });

'''

''' -------- JD登录:
 登录 URL: https://passport.jd.com/new/login.aspx?ReturnUrl=https://trade.jr.jd.com/centre/browse.action
 登陆后的页面是: 个人页面: https://trade.jr.jd.com/centre/browse.action

 登录 URL: https://passport.jd.com/new/login.aspx
 登陆后的页面是: 首页: https://jd.com
'''

''' URL 学习
URL由三部分组成：资源类型、存放资源的主机域名、资源文件名。
URL的一般语法格式为：(带方括号[]的为可选项)：
protocol :// hostname [端口] / path / [参数][?query]#fragment
(传输协议)://(存放资源的服务器的主机名/域名/IP地址)(端口)/(路径:用来表示主机上的一个目录)
/(参数:特殊参数)(参数:?aa=bb&cc=dd)#(定位到指定某一部分信息片段)
'''

'''
如何生成二维码图片:
查看二维码的标签: qr.m.jd.com/show?appid=133&size=147&t=1495786022578
其中 t,就是时间戳.
分解: url = qr.m.jd.com,参数=appid=133&size=147&t=1495786022578
<div class="qrcode-img">
    <img src="//qr.m.jd.com/show?appid=133&size=147&t=1495786022578" alt="">
</div>

'''

''' JD 扫码登录的基本流程

    1. 要获取到 QR;
    2. 要定时检测是否登录成功;
    3. 登录成功后,将 cookie 保存, 然后加载指定的页面.

    其中主要依靠抓包来获取到上述的详细细节.
    打开https://passport.jd.com/new/login.aspx,
    然后在抓包工具中查看, 和二维码相关的URL就是: https://qr.m.jd.com
    1. 获取二维码生成: URL 抓包工具可以直接看到:https://qr.m.jd.com/show?appid=133&size=147&t=1495792203610
    (也可以通过 JD html 页面查看标签的.)

    2. 定时检查登录成功的 url,需要通过抓包工具看定时请求的 url即可:
    定时请求的URL:并携带的有 cookie.
    https://qr.m.jd.com/check?callback=jQuery4435003&appid=133&token=o79axmcc5ijpbjnzidjjdrzaxjt6mzwa&_=1495792266985
    并且,这个 URL 会返回响应结果:jQuery5490864({ "code" : 201, "msg" : "二维码未扫描 ，请扫描二维码"})
    可见,当 app扫码登录后, 请求上述的 URL 会直接返回请求的结果.
    其中参数如下:
    callback=jQuery4435003 这个是每次都不一样, 应该是一个随机数.
    appid=133  这个是固定的
    token=o79axmcc5ijpbjnzidjjdrzaxjt6mzwa 这个是之前页面携带的 token
    _=1495792266985 这个应该是时间戳.
    OK. 完事具备, 开工.

定时请求二维码扫描状态的请求头.其中referer 必须

:method: GET
:path: /check?callback=jQuery970183&appid=133&token=8xagb276e6djivh9k9psdnomra3y00b9&_=1495793204876
:authority: qr.m.jd.com
:scheme: https
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0
accept: */*
accept-language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
accept-encoding: gzip, deflate, br
referer: https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F
cookie: __jda=122270672.14948218443232036061250.1494821844.1494825758.1495792167.3
cookie: __jdv=122270672|direct|-|none|-|1494821844325
cookie: __jdu=14948218443232036061250
cookie: TrackID=1n-fxq5D0g9EUuJnwa5kXUffZ2iiYcZzt8kLp2yRDXEgosjG_Rt6y4WnKx9HJS0ie3a5i0aaU8RLFG9bDDmc-pdUf1A44DuL36CnADIXgB9o5Q8TXzio2irZ2nenAOVgp
cookie: pinId=V7jlz-L9KD0BNB2Km3viKQ
cookie: unick=%E7%BD%91%E8%B4%ADsir
cookie: _tp=iNWy%2FTJel8qoiJsI8sGR9oc868TPppOeV6T5aW%2F1ugI%3D
cookie: _pst=%E7%BD%91%E8%B4%ADsir
cookie: __jdb=122270672.3.14948218443232036061250|3.1495792167
cookie: __jdc=122270672
cookie: QRCodeKey=AAEAID0BnFq38MWfAQ_4B-TQcucuBR16U0wvhP0i06Zn-JSY
cookie: wlfstk_smdl=8xagb276e6djivh9k9psdnomra3y00b9
cookie: _jrda=1
cookie: _jrdb=1495792208731
cookie: 3AB9D23F7A4B3C9B=ZLDU3MWDLEJUB4HASPXBC2ZXJEQTS72KZTHAWO73BNE4QTTK2JGEDTLSVYBDTAD2YUIZELCHVGX55CC7R2NXVB7U5A


'''

class JDWrapper(object):

    def __init__(self,usr_name=None,usr_pwd=None):

        self.usr_name = usr_name
        self.usr_pwd = usr_pwd
        #请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'ContentType': 'text/html; charset=utf-8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',

        }
        #保存 cookie
        self.cookies = {

        }
        # requests.Session()会话对象能够实现跨请求保持某些参数。它也会在同一个 Session 实例发出的所有请求之间保持 cookie
        self.sess = requests.Session()
        # 处理代理错误: Caused by ProxyError('Cannot connect to proxy.'
        # trust_env:取用系統環境變數 =False，將忽略以下系統參數:系統的 proxys/.netrc 的身份認證/定義在 REQUESTS_CA_BUNDLE 中的 CA bundles CURL_CA_BUNDLE
        self.sess.trust_env = False

    def login_by_QR(self):

        try:
            print ('++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print (u'{0} 请打开京东手机客户端,准备扫码登录:'.format(time.ctime()))
            urls = (
                'https://passport.jd.com/new/login.aspx',
                'https://qr.m.jd.com/show',#生成二维码的 url,参见如上的解说
                'https://qr.m.jd.com/check',#检查二维码是否被扫描
                'https://passport.jd.com/uc/qrCodeTicketValidation'
            )
            #1-1-创建登录请求
            resp = self.sess.get(
                urls[0],
                headers=self.headers
            )
            # print (resp.cookies.status_code)
            #1-2-判断登录是否成功
            if resp.status_code != requests.codes.OK:
                print(u'获取登录页面失败:%u',resp.status_code)
                return False

            #1-3- save cookie
            for k,v in resp.cookies.items():
                self.cookies[k]=v

            #1-4- 获取二维码图片:
            resp = self.sess.get(
                urls[1],
                headers=self.headers,
                cookies=self.cookies,
                params={
                    'appid':133,
                    'size':147,
                    't':(int)(time.time()*1000)
                }
            )
            #1-5-判断二维码获取状态
            if resp.status_code != requests.codes.OK:
                print (u'获取二维码失败:%u',resp.status_code)
                return False
            #1-6-save cookie
            for k,v in resp.cookies.items():
                self.cookies[k]=v

            #1-7- save QR
            image_file  = 'qr.png' #os.path.join(os.getcwd(), 'jd_qr.png')

            with open(image_file,'wb') as f: # wb 以二进制写模式打开. rb 以二进制读模式打开
                for chunk in resp.iter_content(chunk_size=1024):
                    f.write(chunk)

            #1-8- 开始扫描二维码:
            os.system('start ' + image_file)

            self.headers['Host'] ='qr.m.jd.com'
            self.headers['Referer'] ='https://passport.jd.com/new/login.aspx'
            qr_ticket = None
            retry_times = 100
            while retry_times:
                retry_times -= 1
                resp = self.sess.get(
                    urls[2],
                    headers=self.headers,
                    cookies=self.cookies,
                    # 参数参见如上的分析
                    params={
                        'callback':'jQuery%u' % random.randint(100000, 999999),
                        'appid':133,
                        'token':self.cookies['wlfstk_smdl'],
                        '_':(int)(time.time()*1000)
                    }
                )
                #状态的判断
                if resp.status_code != requests.codes.OK:
                    continue
                print ('6666666'+resp.text+'666666')
                n1 = resp.text.find('(')
                n2 = resp.text.find(')')
                # json.loads() 将一个JSON编码的字符串转换回一个Python数据结构：
                rs = json.loads(resp.text[n1+1:n2])
                if rs['code'] == 200:
                    print (u'成功状态码:{} :  ticket:{}'.format(rs['code'], rs['ticket']))
                    qr_ticket = rs['ticket']
                    break
                else:
                    print (u'状态码:{} --- 消息:{}'.format(rs['code'], rs['msg']))
                    time.sleep(3)
            if not qr_ticket:
                print ('二维码登录失败')
                return  False

            self.headers['Host'] = 'passport.jd.com'
            self.headers['Referer'] = 'https://passport.jd.com/uc/login?ltype=logout'
            resp = self.sess.get(
                urls[3],
                headers=self.headers,
                cookies=self.cookies,
                params={'t': qr_ticket},
            )
            if resp.status_code != requests.codes.OK:
                print (u'二维码登录失败,状态码:%u',resp.status_code)
                return False

            self.headers['P3P'] = resp.headers.get('P3P')
            for (k,v) in resp.cookies.items():
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
        resp = self.sess.get(
            stock_link)
        soup = bs4.BeautifulSoup(resp.text, "html.parser")
        f = open(os.path.join(os.getcwd(), "我的购物车页面.txt"), 'a+')
        f.writelines(soup.prettify())
        f.close()

        # 我的关注页面:
        stock_link2 = 'https://t.jd.com/home/follow'
        resp2 = self.sess.get(
            stock_link2, )
        soup2 = bs4.BeautifulSoup(resp2.text, "html.parser")
        f = open(os.path.join(os.getcwd(), "关注页面.txt"), 'a+')
        f.writelines(soup.prettify())
        f.close()

        # 我的订单页面:
        stock_link3 = 'https://order.jd.com/center/list.action?search=0&d=2&s=4096'
        resp3 = self.sess.get(
            stock_link3)
        soup3 = bs4.BeautifulSoup(resp3.text, "html.parser")
        f = open(os.path.join(os.getcwd(), "订单页面.txt"), 'a+')
        f.writelines(soup.prettify())
        f.close()

        # list all goods detail in cart
        cart_url = 'https://cart.jd.com/cart.action'
        cart_header = u'购买    数量    价格        总价        商品'
        cart_format = u'{0:8}{1:8}{2:12}{3:12}{4}'

        resp = self.sess.get(cart_url, cookies=self.cookies)
        resp.encoding = 'utf-8'
        soup = bs4.BeautifulSoup(resp.text, "html.parser")

        print ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print (u'{0} >>>>>>>>>>>>>>>>>>>>>> 购物车明细'.format(time.ctime()))
        print (resp.text)




            # def main(options):
    #
jd = JDWrapper()
jd.login_by_QR()
        # return

jd.getPage()


#
#
# if __name__ == '__main__':
#
#     # get_cur_info()
#
#     parser = argparse.ArgumentParser(description='Simulate to login Jing Dong, and buy sepecified good')
#
#
#     options = parser.parse_args()
#     print (options)
#
#     main(options)





















