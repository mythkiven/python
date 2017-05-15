#-*_coding:utf8-*-
# -*- coding: utf-8 -*-
# coding=utf-8


import requests
import re
# 网页默认是utf-8 windows系统默认是GBK,直接爬取的数据会有乱码的
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import xlrd
import xlwt
import time,datetime
from xlutils.copy import copy
from xlrd import open_workbook
from xlwt import easyxf

# 宏定义数据
path = "/Users/guoyinjinrong1/百度云同步盘/MAC电脑间的同步/基金/data.xls"
path2 = "/Users/guoyinjinrong1/百度云同步盘/MAC电脑间的同步/基金/"
url = 'http://www.jjmmw.com/fund/sypm/?order=1year&limit=0'
# 储存的日期 已编码
timeNow = time.strftime('%Y-%m-%d %Hh', time.localtime(time.time()))
# 今天日期  已编码
timeT = time.strftime('%Y-%m-%d', time.localtime(time.time()))
# 前一天日期 已编码
timeP = time.strftime('%Y-%m-%d', time.localtime(time.time()-24*60*60))
''
''
# 股票型 url = http://www.jjmmw.com/fund/sypm/?string=gp&order=1year&limit=0
# 全部的数据


class spider(object):
    def __init__(self):
        print '开始爬取内容。。。'

    # getsource用来获取网页源代码
    def getsource(self, url):
        html = requests.get(url)
        return html.text

    # changepage用来生产不同页数的链接
    #     def changepage(self,url,total_page):
    #         now_page = int(re.search('pageNum=(\d+)',url,re.S).group(1))
    #         page_group = []
    #         for i in range(now_page,total_page+1):
    #             link = re.sub('pageNum=\d+','pageNum=%s'%i,url,re.S)
    #             page_group.append(link)
    #         return page_group
    # geteveryclass用来抓取每个课程块的信息 <
    def getmaintext(self, source):
        everyclass = re.search(
            '(<table width="950" border="0" align="center" cellpadding="0" cellspacing="0" class="table02" id="fundlist" data-lt="sypm">.*?</table>)',
            source, re.S).group(1)
        return everyclass

    def geteveryclass(self, source):
        maintext = re.findall('(<td class="t13".*?</td></tr>)', source, re.S)
        return maintext

    # getinfo用来从每个课程块中提取出我们需要的信息
    def getinfo(self, eachclass):
        info = {}
        info["num"] = re.search('<td width="3%" align="center">(.*?)</td>', eachclass, re.S).group(1)
        info["id"] = re.search('target="_blank">(.*?)</a></td>', eachclass, re.S).group(1)
        info['name'] = re.search('target="_blank" class="blue ellipsis" title="(.*?)">', eachclass, re.S).group(1)
        info['time'] = re.search('<td width="7%" align="center">(.*?)</td>', eachclass, re.S).group(1)
        info["price1"] = re.findall('<td width="6%" align="center">(.*?)</td>', eachclass, re.S)[1]
        info["price2"] = re.findall('<td width="6%" align="center">(.*?)</td>', eachclass, re.S)[2]

        # info["zengRi"] = re.search('<td width="7%" align="center"><span class="red">(.*?)</span></td>',eachclass,re.S).group(1)
        # info["zengZhou"] = re.findall('<td width="5%" align="center"><span class="red">(.*?)</span></td>',eachclass,re.S)[0]
        # info["zengYue"] = re.findall('<td width="5%" align="center"><span class="red">(.*?)</span></td>',eachclass,re.S)[1]
        # info["zeng3Yue"] = re.findall('<td width="5%" align="center"><span class="red">(.*?)</span></td>',eachclass,re.S)[2]
        # info["zeng6Yue"] = re.findall('<td width="5%" align="center"><span class="red">(.*?)</span></td>',eachclass,re.S)[3]
        # info["zengNian"] = re.findall('<td width="5%" align="center"><span class="red">(.*?)</span></td>',eachclass,re.S)[4]
        # info["zengJin"] = re.findall('<td width="5%" align="center"><span class="red">(.*?)</span></td>',eachclass,re.S)[5]
        # info["zengChenli"] = re.findall('<td width="5%" align="center"><span class="red">(.*?)</span></td>',eachclass,re.S)[6]


        return info

    # saveinfo用来保存结果到info.txt文件中
    def saveinfo(self, classinfo):

        # 写入文本:
        # r:读 w:写 a:追加 b:二进制(可添加在其他模式) +:读写(可添加在其他模式)
        f = open("/Users/guoyinjinrong1/百度云同步盘/MAC电脑间的同步/基金/" + "2" + ".txt", 'a+')
        for each in classinfo:
            f.writelines('xuhao:' + each['num'] + '\n')
            f.writelines('daima:' + each['id'] + '\n')
            f.writelines('name:' + each['name'] + '\n')
            f.writelines('time:' + each['time'] + '\n')
            f.writelines('price1:' + each['price1'] + '\n')
            f.writelines('price2:' + each['price2'] + '\n')
            f.writelines('url:http://www.jjmmw.com/fund/' + each['id'] + '/' + '\n\n')
            # f.writelines('日增长率:' + each['zengRi'] + '\n')
            # f.writelines('近1周:' + each['zengZhou'] + '\n')
            # f.writelines('近1月:' + each['zengYue'] + '\n')
            # f.writelines('近3月:' + each['zeng3Yue'] + '\n')
            # f.writelines('近6月:' + each['zeng6Yue'] + '\n')
            # f.writelines('近1年:' + each['zengNian'] + '\n')
            # f.writelines('今年来:' + each['zengJin'] + '\n')
            # f.writelines('成立以来:' + each['zengChenli'] + '\n\n')
        f.close()

        #         # 写入excel:
        #
        #         style = xlwt.XFStyle()  # 初始化样式
        #         font = xlwt.Font()  # 为样式创建字体
        #         font.name = 'Times New Roman'  # 'Times New Roman'
        #         book = xlwt.Workbook(encoding='utf-8',style_compression=0)
        #         sheet = book.add_sheet(timeNow,cell_overwrite_ok=True)
        #         i = 1
        #         fir = ["序号","链接","代码","名称","时间","单位净值","累计净值"]
        #         for k in range(0,7):
        #             sheet.write(0,k,fir[k])
        #         for each in classinfo:
        #             sheet.write(i, 0, each['num'])
        #             sheet.write(i, 1, 'http://www.jjmmw.com/fund/' + each['id'] + '/')
        #             sheet.write(i, 2, each['id'])
        #             sheet.write(i, 3, each['name'])
        #             sheet.write(i, 4, each['time'])
        #             sheet.write(i, 5, each['price1'])
        #             sheet.write(i, 6, each['price2'])
        #             i+=1
        #         book.save(path)
        # #
        # # # 读写操作: 在现有的excel上进行读写:
        #     def duxie(self):


        rb = open_workbook(path, formatting_info=True)
        r_sheet = rb.sheet_by_index(0)  # read only copy to introspect the file
        wb = copy(rb)  # a writable copy (I can't read values out of this, only write to it)
        sheet = wb.get_sheet(0)  # the sheet to write to within the writable copy
        j = r_sheet.ncols
        i = 1
        timeShould = timeP
        timeQ =  timeP
        tListB = []
        tListS = []
        # fir = ["代码","时间","单位净值","累计净值","写入时间"]
        fir = ["ID", "Time", "NowPrice", "PlusPrice", "WriteTime"]

        # 写入基金4数据
        for each in classinfo:
            sheet.write(i, j + 0, each['id'])
            sheet.write(i, j + 1, each['time'])
            sheet.write(i, j + 2, each['price1'])
            sheet.write(i, j + 3, each['price2'])
            i += 1
            timeQ = each['time']
            if timeQ > timeShould:
                print timeQ
                tListB.append(each['id']+' '+timeQ)
            elif timeQ < timeShould:
                print timeQ
                tListS.append(each['id']+' '+timeQ)
            else:
                print
        # 写入额外信息
        for k in range(j, j + 5):
            sheet.write(0, k, fir[k - j])
            print k
            if k == j + 4:
                sheet.write(1, k, timeNow)
                sheet.write(2,k,"UNupdate:"+str(len(tListS)))

        print "未及时更新列表:"
        print tListS
        print "数量:"+str(len(tListS))
        print "数据错误列表:"
        print tListB

        wb.save(path)


# 判断写入的时间是否已经存在:
def read_excel():
    rb = open_workbook(path, formatting_info=True)
    r_sheet = rb.sheet_by_index(0)
    # 遍历第2行所有列,是否有时间数据c
    print "\n已经爬取的列数:" + str(r_sheet.ncols) + "\n"
    for c in range(0, r_sheet.ncols):
        age_nov = r_sheet.cell(1, c).value
        print age_nov
        if ((c + 1) % 5 == 0) and (c != 0):
            print "\n"
        if age_nov == timeNow:
            return 1
    else:
        return 0

# 获取今天应该更新的日期:周2-6为前一天,周日,周一不更新
def getTime():
    timeToday = datetime.date.today()
    zhouji = timeToday.weekday()
    if zhouji>=2 and zhouji<=6:
        return timeT #返回已经编码的日期
    else:
        print "今天是周日或者周一,不获取信息。周六获取周五,周二获取周一的信息"
        return 0


if __name__ == '__main__':
    classinfo = []

    # 首先判断时间是否满足:
    if getTime() ==0:
        exit()

    jikespider = spider()
    print u'正在处理页面：' + url
    html = jikespider.getsource(url)
    maint = jikespider.getmaintext(html)
    everyclass = jikespider.geteveryclass(maint)

    for each in everyclass:
        info = jikespider.getinfo(each)
        classinfo.append(info)

    if read_excel():
        print "\n 已经爬取过数据!!!"
    else:
        jikespider.saveinfo(classinfo)










'''
#-*_coding:utf8-*-
# -*- coding: utf-8 -*-
import requests
import re

# 网页默认是utf-8 windows系统默认是GBK,直接爬取的数据会有乱码的
import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
import xlrd
import  xlwt
import  time
from xlutils.copy import copy # http://pypi.python.org/pypi/xlutils
from xlrd import open_workbook # http://pypi.python.org/pypi/xlrd
from xlwt import easyxf # http://pypi.python.org/pypi/xlwt

#股票型 url = http://www.jjmmw.com/fund/sypm/?string=gp&order=1year&limit=0
# 全部的数据


class spider(object):
    def __init__(self):
        print '开始爬取内容。。。'

# getsource用来获取网页源代码
    def getsource(self,url):
        html = requests.get(url)
        return html.text

# changepage用来生产不同页数的链接
#     def changepage(self,url,total_page):
#         now_page = int(re.search('pageNum=(\d+)',url,re.S).group(1))
#         page_group = []
#         for i in range(now_page,total_page+1):
#             link = re.sub('pageNum=\d+','pageNum=%s'%i,url,re.S)
#             page_group.append(link)
#         return page_group
# geteveryclass用来抓取每个课程块的信息 <
    def getmaintext(self,source):
        everyclass = re.search('(<table width="950" border="0" align="center" cellpadding="0" cellspacing="0" class="table02" id="fundlist" data-lt="sypm">.*?</table>)',source,re.S).group(1)
        return everyclass
    def geteveryclass(self,source):
        maintext = re.findall('(<td class="t13".*?</td></tr>)',source,re.S)
        return maintext
# getinfo用来从每个课程块中提取出我们需要的信息
    def getinfo(self,eachclass):
        info = {}
        info["num"]  = re.search('<td width="3%" align="center">(.*?)</td>',eachclass,re.S).group(1)
        info["id"] = re.search('target="_blank">(.*?)</a></td>',eachclass,re.S).group(1)
        info['name'] = re.search('target="_blank" class="blue ellipsis" title="(.*?)">',eachclass,re.S).group(1)
        info['time'] = re.search('<td width="7%" align="center">(.*?)</td>',eachclass,re.S).group(1)
        info["price1"] = re.findall('<td width="6%" align="center">(.*?)</td>',eachclass,re.S)[1]
        info["price2"] = re.findall('<td width="6%" align="center">(.*?)</td>',eachclass,re.S)[2]

        # info["zengRi"] = re.search('<td width="7%" align="center"><span class="red">(.*?)</span></td>',eachclass,re.S).group(1)
        # info["zengZhou"] = re.findall('<td width="5%" align="center"><span class="red">(.*?)</span></td>',eachclass,re.S)[0]
        # info["zengYue"] = re.findall('<td width="5%" align="center"><span class="red">(.*?)</span></td>',eachclass,re.S)[1]
        # info["zeng3Yue"] = re.findall('<td width="5%" align="center"><span class="red">(.*?)</span></td>',eachclass,re.S)[2]
        # info["zeng6Yue"] = re.findall('<td width="5%" align="center"><span class="red">(.*?)</span></td>',eachclass,re.S)[3]
        # info["zengNian"] = re.findall('<td width="5%" align="center"><span class="red">(.*?)</span></td>',eachclass,re.S)[4]
        # info["zengJin"] = re.findall('<td width="5%" align="center"><span class="red">(.*?)</span></td>',eachclass,re.S)[5]
        # info["zengChenli"] = re.findall('<td width="5%" align="center"><span class="red">(.*?)</span></td>',eachclass,re.S)[6]


        return info
# saveinfo用来保存结果到info.txt文件中
    def saveinfo(self,classinfo):
        path = "/Users/guoyinjinrong1/百度云同步盘/MAC电脑间的同步/基金/data.xls"
        path2 = "/Users/guoyinjinrong1/百度云同步盘/MAC电脑间的同步/基金/"
        url = 'http://www.jjmmw.com/fund/sypm/?order=1year&limit=0'
        timeNow = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        # 写入文本:
        # r:读 w:写 a:追加 b:二进制(可添加在其他模式) +:读写(可添加在其他模式)
        f = open("/Users/guoyinjinrong1/百度云同步盘/MAC电脑间的同步/基金/"+"2"+".txt",'a+')
        for each in classinfo:
            f.writelines('xuhao:' + each['num'] + '\n')
            f.writelines('daima:' + each['id'] + '\n')
            f.writelines('name:' + each['name'] + '\n')
            f.writelines('time:' + each['time'] + '\n')
            f.writelines('price1:' + each['price1'] + '\n')
            f.writelines('price2:' + each['price2'] + '\n')
            f.writelines('url:http://www.jjmmw.com/fund/'+each['id']+'/'+'\n\n')
            # f.writelines('日增长率:' + each['zengRi'] + '\n')
            # f.writelines('近1周:' + each['zengZhou'] + '\n')
            # f.writelines('近1月:' + each['zengYue'] + '\n')
            # f.writelines('近3月:' + each['zeng3Yue'] + '\n')
            # f.writelines('近6月:' + each['zeng6Yue'] + '\n')
            # f.writelines('近1年:' + each['zengNian'] + '\n')
            # f.writelines('今年来:' + each['zengJin'] + '\n')
            # f.writelines('成立以来:' + each['zengChenli'] + '\n\n')
        f.close()

#         # 写入excel:
#
#         style = xlwt.XFStyle()  # 初始化样式
#         font = xlwt.Font()  # 为样式创建字体
#         font.name = 'Times New Roman'  # 'Times New Roman'
#         book = xlwt.Workbook(encoding='utf-8',style_compression=0)
#         sheet = book.add_sheet(timeNow,cell_overwrite_ok=True)
#         i = 1
#         fir = ["序号","链接","代码","名称","时间","单位净值","累计净值"]
#         for k in range(0,7):
#             sheet.write(0,k,fir[k])
#         for each in classinfo:
#             sheet.write(i, 0, each['num'])
#             sheet.write(i, 1, 'http://www.jjmmw.com/fund/' + each['id'] + '/')
#             sheet.write(i, 2, each['id'])
#             sheet.write(i, 3, each['name'])
#             sheet.write(i, 4, each['time'])
#             sheet.write(i, 5, each['price1'])
#             sheet.write(i, 6, each['price2'])
#             i+=1
#         book.save(path)
# #
# # # 读写操作: 在现有的excel上进行读写:
#     def duxie(self):
        path = "/Users/guoyinjinrong1/百度云同步盘/MAC电脑间的同步/基金/data.xls"

        rb = open_workbook(path, formatting_info=True)
        r_sheet = rb.sheet_by_index(0)  # read only copy to introspect the file
        wb = copy(rb)  # a writable copy (I can't read values out of this, only write to it)
        sheet = wb.get_sheet(0)  # the sheet to write to within the writable copy
        j = r_sheet.ncols
        i = 1
        # fir = ["代码","时间","单位净值","累计净值","写入时间"]
        fir = ["ID", "Time", "NowPrice", "PlusPrice", "WriteTime"]
        for k in range(j, j + 5):
            sheet.write(0, k, fir[k - j])
            print k
            if k == j + 4:
                sheet.write(1, k, timeNow)
        for each in classinfo:
            sheet.write(i, j+0, each['id'])
            sheet.write(i, j+1, each['time'])
            sheet.write(i, j+2, each['price1'])
            sheet.write(i, j+3, each['price2'])
            i += 1

        wb.save(path)


#   判断写入的时间是否已经存在:
def read_excel():
    timeNow = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    path = "/Users/guoyinjinrong1/百度云同步盘/MAC电脑间的同步/基金/data.xls"
    rb = open_workbook(path, formatting_info=True)
    r_sheet = rb.sheet_by_index(0)
    # 遍历第2行所有列,是否有时间数据c
    print "\n已经爬取的列数:"+str(r_sheet.ncols)+"\n"
    for c in range(0,r_sheet.ncols):

        age_nov = r_sheet.cell(1, c).value
        print age_nov
        if ((c+1)%5 == 0)and(c!=0):
            print "\n"

        if age_nov == timeNow:
             return 1
    else:
        return 0




if __name__ == '__main__':
    url = 'http://www.jjmmw.com/fund/sypm/?order=1year&limit=0'
    classinfo = []


    jikespider = spider()
    # all_links = jikespider.changepage(url,2)
    # for link in all_links:
    print u'正在处理页面：' + url
    html = jikespider.getsource(url)
    # print html
    maint = jikespider.getmaintext(html)
    # f = open('main2.text', 'a+')
    # f.writelines(maint)
    # f.close()
    # print maint
    everyclass = jikespider.geteveryclass(maint)

    for each in everyclass:
        info = jikespider.getinfo(each)
        classinfo.append(info)
    #
    if read_excel():
        print "\n 已经爬取过数据!!!"
    else:
        jikespider.saveinfo(classinfo)


'''











