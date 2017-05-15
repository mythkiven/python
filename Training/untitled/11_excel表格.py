#coding = utf-8
# -*- coding: utf-8 -*-



''''''
'''
python操作excel主要用到xlrd和xlwt这两个库，即xlrd是读excel，xlwt是写excel的库。
可从这里下载https://pypi.python.org/pypi。

1、python读excel——xlrd

'''
from xlutils.copy import copy  # http://pypi.python.org/pypi/xlutils
from xlrd import open_workbook  # http://pypi.python.org/pypi/xlrd
from xlwt import easyxf  # http://pypi.python.org/pypi/xlwt
import time
import xlrd
import xlwt
import xlutils
from datetime import date, datetime
from xlutils.copy import copy

def read_excel():
    work = xlrd.open_workbook('demo1.xls')
    sheet = work.sheet_names()
    print sheet
    t = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    t = "2222"
    for element in sheet:
        if t==element:
            return 1
    else:
        return 0

'''
设置单元格样式
'''


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    # borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6

    style.font = font
    # style.borders = borders

    return style


# 写excel
def write_excel():
    # f = xlutils.open_workbook('demo1.xls')
    # sheet = f.sheet_names()
    # t = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # t = "2222"
    # for element in sheet:
    #     if t == element:
    #         return
    # else:
    #     return 0
    #
    # oldWb = xlrd.open_workbook(gConst['xls']['fileName'], formatting_info=True);
    # print oldWb;  # <xlrd.book.Book object at 0x000000000315C940>
    # newWb = copy(oldWb);
    # print newWb;  # <xlwt.Workbook.Workbook object at 0x000000000315F470>
    # newWs = newWb.get_sheet(0);
    # newWs.write(1, 0, "value1");
    # newWs.write(1, 1, "value2");
    # newWs.write(1, 2, "value3");
    # print "write new values ok";
    # newWb.save(gConst['xls']['fileName']);

    f = xlwt.Workbook()  # 创建工作簿


    '''
    创建第一个sheet:
      sheet1
    '''
    t = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    t ="2211111122"
    sheet1 = f.add_sheet(t, cell_overwrite_ok=True)  # 创建sheet
    row0 = [u'业务', u'状态', u'北京', u'上海', u'广州', u'深圳', u'状态小计', u'合计']
    column0 = [u'机票', u'船票', u'火车票', u'汽车票', u'其它']
    status = [u'预订', u'出票', u'退票', u'业务小计']

    # 生成第一行
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))

    # 生成第一列和最后一列(合并4行)
    i, j = 1, 0
    while i < 4 * len(column0) and j < len(column0):
        sheet1.write_merge(i, i + 3, 0, 0, column0[j], set_style('Arial', 220, True))  # 第一列
        sheet1.write_merge(i, i + 3, 7, 7)  # 最后一列"合计"
        i += 4
        j += 1

    sheet1.write_merge(21, 21, 0, 1, u'合计', set_style('Times New Roman', 220, True))

    # 生成第二列
    i = 0
    while i < 4 * len(column0):
        for j in range(0, len(status)):
            sheet1.write(j + i + 1, 1, status[j])
        i += 4

    '''
      创建第二个sheet:
        sheet2
      '''
    t = '3331111113333'
    sheet2 = f.add_sheet(t, cell_overwrite_ok=True)  # 创建sheet2
    row0 = [u'姓名', u'年龄', u'出生日期', u'爱好', u'关系']
    column0 = [u'小杰', u'小胖', u'小明', u'大神', u'大仙', u'小敏', u'无名']

    # 生成第一行
    for i in range(0, len(row0)):
        sheet2.write(0, i, row0[i], set_style('Times New Roman', 220, True))

    # 生成第一列
    for i in range(0, len(column0)):
        sheet2.write(i + 1, 0, column0[i], set_style('Times New Roman', 220))

    sheet2.write(1, 2, '1991/11/11')
    sheet2.write_merge(7, 7, 2, 4, u'暂无')  # 合并列单元格
    sheet2.write_merge(1, 2, 4, 4, u'好朋友')  # 合并行单元格


    f.save('demo1.xls')  # 保存文件


def duxie(index,indexj):
    # 读写操作:

    START_ROW = 0  # 0 based (subtract 1 from excel row number)
    col_age_november = 1
    col_summer1 = index
    col_fall1 = indexj

    rb = open_workbook('demo1.xls', formatting_info=True)
    r_sheet = rb.sheet_by_index(0)  # read only copy to introspect the file
    wb = copy(rb)  # a writable copy (I can't read values out of this, only write to it)
    w_sheet = wb.get_sheet(0)  # the sheet to write to within the writable copy
    print w_sheet
    # for row_index in range(START_ROW, r_sheet.nrows):
    #     # 行内容
    #     age_nov = r_sheet.cell(row_index, col_age_november).value
    #
    #     if 2:
    #         # If 3, then Combo I 3-4 year old  for both summer1 and fall1
    #         w_sheet.write(row_index, col_summer1, '21')
    #         w_sheet.write(row_index, col_fall1, '21')
    wb.save('demo1.xls')


if __name__ == '__main__':
    # generate_workbook()
    # read_excel()
    # if read_excel():
    #     print "have"
    # else:
    #      write_excel()
    for i in  range(15,16):
        duxie(i,i+2)


