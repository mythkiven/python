# coding=utf-8

# 三方库的安装:
# 少用easy_install 因为只能安装不能卸载
# 多用pip方式安装

''' '''
'''
爬虫的基本原理:
1、首先用request获取网页源码,
2、然后用正则表达式获取我们需要的内容

request方法:
1、直接获取源码;
2、修改http头获取源码
3、向网页提交数据
    Get是从服务器上获取数据
    Post是向服务器传送数据
    Get通过构造url中的参数来实现功能
    Post将数据放在header提交数据
Post:
核心方法：request.post
核心步骤：构造表单-提交表单-获取返回信息


Requests获取网页源代码
修改Http头绕过简单的反扒虫机制
向网页提交内容


'''


import re
import requests

# 1、获取百度贴吧的源码
htmll =  requests.get('http://tieba.baidu.com/f?ie=utf-8&kw=python')
# print htmll.text





# 2、修改http头来爬取源码
# 下面三行是编码转换的功能，大家现在不用关心。
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# hea是我们自己构造的一个字典，里面保存了user-agent
hea = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
# html = requests.get('http://jp.tingroom.com/yuedu/yd300p/')
html = requests.get('http://jp.tingroom.com/yuedu/yd300p/',headers = hea)
# 下面这一行是将编码转为utf-8否则中文会显示乱码。
html.encoding = 'utf-8'
# 网页源码
# print html.text
print "\n"*3
# 获取想要的内容
# title = re.findall('color:#666666;">(.*?)</span>',html.text,re.S)
# for each in title:
    # print each

print "\n"*3

# chinese = re.findall('color: #039;">(.*?)</a>',html.text,re.S)
# for each in chinese:
    # print each






# 3、表单提交

# url = 'https://www.crowdfunder.com/browse/deals'
url = 'https://www.crowdfunder.com/browse/deals&template=false'
# html = requests.get(url).text
# print html

#注意这里的page后面跟的数字需要放到引号里面。
data = {
    'entities_only':'true',
    'page':'1'
}
html_post = requests.post(url,data=data)
title = re.findall('"card-title">(.*?)</div>',html_post.text,re.S)
for each in title:
    print each


