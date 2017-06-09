# encoding:utf-8


# 导入模块:
import sys
import requests #网络模块
import os   #系统模块
import time # 日期模块
import json # json 解析
import random #随机数模块
import bs4 # 解析网页
import pickle



# 注意,cookielib 归入http.cookiejar中
# try:
#     from http.cookiejar import MozillaCookieJar
# except ImportError:
#     from cookielib import MozillaCookieJar


# 匿名函数: 打印当前函数信息
FuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name

# 解析方法
def tags_val(tag, key='',index=0):
    '''
    return html tag list attribute @key @index
    if @key is empty, return tag content
    '''
    if len(tag) == 0 or len(tag) <= index:
        return ''
    elif key:
        txt = tag[index].get(key)
        # strip(aa):移除字符串头尾指定的字符aa, 移除各种空格换行
        return txt.strip(' \t\r\n') if txt else ''
    else:
        txt = tag[index].text
        return txt.strip(' \t\r\n') if txt else ''
# 解析方法
def tag_val(tag, key=''):
    '''
    return html tag attribute @key
    if @key is empty, return tag content
    '''
    if tag is None:
        return ''
    elif key:
        txt = tag.get(key)
        return txt.strip(' \t\r\n') if txt else ''
    else:
        txt = tag.text
        return txt.strip(' \t\r\n') if txt else ''

# 定义JD类 扫码登录类:
class JDLoginByQR():

    # 初始化
    def __init__(self):

        self.request = requests.Session()
        self.cookieFile = "JD_QR_Cookies.txt"
        self.loginUrl = 'https://passport.jd.com/new/login.aspx'
        # 个人页面,用户校验 cookie是否有效
        self.homeUrl = 'http://home.jd.com/'
        # 处理SSL,代理错误: Caused by ProxyError('Cannot connect to proxy.'
        # trust_env:取用系統環境變數 =False，
        # 將忽略以下系統參數:系統的 proxys/.netrc 的身份認證/定義在 REQUESTS_CA_BUNDLE 中的 CA bundles CURL_CA_BUNDLE
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

    #  cookie本地文件 检测
    def load_cookies(self):
        # 没有文件=>有文件没有数据=>有文件有数据
        try:
            # 检测文件大小
            if os.path.getsize(self.cookieFile):
                with open(self.cookieFile, 'rb') as f2:
                    self.cookies = pickle.load(f2)
                    print('cookie本地检测: 有文件有数据')
                    return True
            else:
                print('cookie本地检测: 有文件无数据')
        except IOError:
            print('cookie本地检测: 无文件==>创建文件')
            # 创建文件
            os.mknod(self.cookieFile)
            return False

        return False

        # 写法2:
        #
        # f2 = open(self.cookieFile, "rb")
        # try:
        #     self.cookies = pickle.load(f2)
        #     print('cookie本地检测: 成功加载cookie数据', self.cookies)
        # except (Exception) as e:
        #     print('cookie本地检测: 错误: {0} : {1}'.format(FuncName(), e))
        #     return False
        # f2.close()
        # return True

    # 保存cookie数据
    def save_cookies(self):
        f1 = open(self.cookieFile, "wb")
        # 清除之前的数据
        f1.truncate()
        # 写入新数据
        pickle.dump(self.cookies, f1)
        f1.close()

    # cookie 有效性检测
    def checkCookies(self):
        try:
            if self.load_cookies():
                # request默认是可以重定向的, 但是可以通过设置来禁止重定向, 这样,
                #  加载 URLA, 不通,重定向到 URLB, 最终的状态码依然是200.
                #  禁止重定向, 加载 URLA, 不会重新定向, 状态码就是302了.
                resp = self.request.get(self.homeUrl,cookies=self.cookies, allow_redirects=False)
                if resp.status_code == 200:
                    print('cookie有效性校验: 有效')
                else:
                    print('cookie有效性校验: 无效,code:', resp.status_code)
                    return False
            else:
                return  False
        except (Exception) as e:
            print('cookie有效性校验: 错误: {0} : {1}'.format(FuncName(), e))
            return False

        # allow_redirects=True, 允许重定向的话, 可以通过查看响应列表来确定是否有重定向.
        # resp.history ===> 查看 Response 对象列表，我们可以用它来追踪重定向.
        return True


# JD 二维码状态
# 200 ticket:BAEAIJXyLJHeoP5pHnAfrXPuFGiFR_CZS5BiYpANEap7zVZD
# 201 消息:二维码未扫描 ，请扫描二维码
# 202 消息:请手机客户端确认登录
# 203 消息:二维码过期，请重新扫描 => 需要重新加载二维码

    # QR登录
    def login_by_QR(self):

        # 判断cookie 是否存在以及是否有效.
        if self.checkCookies() :
            print('JD登录检测: cookie有效无需扫码')
            return True
        else:
            print('JD登录检测: cookie无效需扫码')


        try:
            print('++++++++++++++++++++++++++++++++++++++++++++++++')
            print(u'{0} >> 请打开 JD 手机客户端,准备扫码登录.'.format(time.time()))
            urls = (
                self.loginUrl,
                'https://qr.m.jd.com/show',
                'https://qr.m.jd.com/check',
                'https://passport.jd.com/uc/qrCodeTicketValidation' #这个是校验登录的
            )

            # 1. 获取登录页面:
            resp = self.request.get(
                urls[0],
                headers=self.headers,
                cookies=self.cookies
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
            print ('二维码登录成功')

            self.save_cookies()

            return True

        except Exception as e:
            print ('Exp:', e)
            raise

        return False


    # 登录检测
    def checkLogin(self):
        # 判断cookie 是否存在以及是否有效.
        if self.login_by_QR():
            print('已登录')
            return True
        else:
            print('尚未登录==>登录')
            if self.login_by_QR():
                print('登录成功!')
                return True
            else:
                print('登录失败!')
                return False

# 我的购物车详情:

    # 购物车
    def getGWCPage(self):

        # 判断是否登陆
        if self.checkLogin():
            print('已登录,开始加载购物车数据')
        else:
            print('未登录,无法加载购物车数据')
            return

        cart_url = 'https://cart.jd.com/cart.action'
        cart_header = u'购买    数量    价格        总价       属性                        商品'
        cart_format = u'{0:6}{1:6}{2:12}{3:12}({4:20}){5}'
        try:
            resp = self.request.get(cart_url,cookies=self.cookies)
            resp.encoding = 'utf-8'
            soup = bs4.BeautifulSoup(resp.text, "html.parser")
            print ('+++++++++++++++++++++++读取购物车明细++++++++++++++++++++++++++++++++')

            f = open(os.path.join(os.getcwd(), "我的购物车页面.html"), 'wt')
            f.writelines(soup.prettify())
            f.close()

            f = open(os.path.join(os.getcwd(), "我的购物车.txt"), 'wt')
            f.writelines(cart_header)
            f.writelines('\n')
            f.close()
            for item in soup.select('div.item-form'):
                check = tags_val(item.select('div.cart-checkbox input'), key='checked')
                check = ' + ' if check else ' - '
                count = tags_val(item.select('div.quantity-form input'), key='value')
                price = tags_val(item.select('div.p-price strong'))
                sums = tags_val(item.select('div.p-sum strong'))
                gname = tags_val(item.select('div.p-name a'))
                propsTxt = tags_val(item.select('div.props-txt'))
                f = open(os.path.join(os.getcwd(), "我的购物单.txt"), 'a+')
                f.writelines(cart_format.format(check, count, price[1:], sums[1:], propsTxt, gname))
                f.writelines('\n')
                f.close()
            t_count = tags_val(soup.select('div.amount-sum em'))
            t_price = tags_val(soup.select('span.sumPrice em'))
            f = open(os.path.join(os.getcwd(), "我的购物单.txt"), 'a+')
            f.writelines('已选:' + t_count + '\n' + '总额:' + t_price)
            f.writelines('\n')
            f.close()
        except (Exception) as e:
            print ('Exp {0} : {1}'.format(FuncName(), e))
#我的订单详情:

    # 订单页面
    def getDDPage(self):

        # 判断是否登陆
        if self.checkLogin():
            print('已登录,开始加载订单数据')
        else:
            print('未登录,无法加载订单数据')
            return

        gwc_url = "http://order.jd.com/center/list.action?search=0&d=2&s=4096"
        gwc_header="购买时间   订单号  商家  数量      价格      支付方式     状态      收货人       商品 "
        cart_format = u'{0:6}{1:6}{2:8}{3:8}{4:8}{5:8}{6:8}{7:8}{8}'
        #今年订单:
        try:
            resp_thisYear = self.request.get(gwc_url,params={'search':'0','d':'2','s':'4096'},)
            resp_thisYear.encoding = 'utf-8'
            soup = bs4.BeautifulSoup(resp_thisYear.text,"html.parser")
            print ('+++++++++++++++读取订单详情+++++++++++++++')

            f = open(os.path.join(os.getcwd(),"我的订单页面.html"),'wt')
            f.writelines(soup.prettify())
            f.close

            f = open(os.path.join(os.getcwd(),"我的订单.txt"),'wt')
            f.writelines(gwc_header)
            f.close

            # 所有的订单都以 tbody形式存在于 table 中.
            for items in soup.select('table.oeder-tb'):
                #时间
                s_time = tags_val(items.select('span.dealtime'))
                #订单号
                s_orderNum = tags_val(items.select('a.orderIdLinks'))
                #商家
                s_orderInfo = tags_val(items.select('span.order-shop span.shop-txt'))
                # 名称
                s_orderName = tags_val(items.select('div.p-name a'))
                #数量
                s_goodsNum = tags_val(items.select('div.goods-number'))
                #收货人
                s_people = tags_val(items.select('div.consignee span.txt'))
                #价格
                s_price = tags_val(items.select('div.amount span'))
                # 支付方式
                s_payW = tags_val(items.select('div.amount span.ftx-13'))
                #状态
                s_status = tags_val(items.select('div.status span.order-status'))
                f = open(os.path.join(os.getcwd(), "我的订单.txt"), 'a+')
                f.writelines(cart_format.format(s_time,s_orderNum,s_orderInfo,s_goodsNum,s_price,s_payW,s_status,s_people,s_orderName))
                f.writelines('\n')
                f.close()

        except (Exception) as e:
            print ('Exp {0} : {1}'.format(FuncName(), e))



def get_locationPages():

    f = open(os.path.join(os.getcwd(), "我的购物车页面.html"), 'r')
    soup = bs4.BeautifulSoup(f.read(), "html.parser")
    cart_header = u'已选    数量    价格        总价       属性                        商品'
    cart_format = u'{0:6}{1:6}{2:12}{3:12}({4:20}){5}'
    print ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    f = open(os.path.join(os.getcwd(), "我的购物单.txt"), 'wt')
    f.writelines(cart_header)
    f.writelines('\n')
    f.close()
    for item in soup.select('div.item-form'):
        #
        check = tags_val(item.select('div.cart-checkbox input'), key='checked')
        check = ' + ' if check else ' - '
        count = tags_val(item.select('div.quantity-form input'), key='value')
        price = tags_val(item.select('div.p-price strong'))
        sums = tags_val(item.select('div.p-sum strong'))
        gname = tags_val(item.select('div.p-name a'))
        propsTxt = tags_val(item.select('div.props-txt'))
        f = open(os.path.join(os.getcwd(), "我的购物单.txt"), 'a+')
        f.writelines(cart_format.format(check, count, price[1:], sums[1:],propsTxt, gname))
        f.writelines('\n')
        f.close()
    t_count = tags_val(soup.select('div.amount-sum em'))
    t_price = tags_val(soup.select('span.sumPrice em'))
    f = open(os.path.join(os.getcwd(), "我的购物单.txt"), 'a+')
    f.writelines('已选商品:'+t_count+'\n'+'商品总额:'+t_price)
    f.writelines('\n')
    f.close()

# 主入口
def main():
    # get_locationPages()

    jd = JDLoginByQR()

    # if not jd.login_by_QR:
    #     return

    jd.getDDPage()
    jd.getGWCPage()

if __name__ == '__main__':

    main()















