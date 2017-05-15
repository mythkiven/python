# coding=utf-8

# 导入re库文件
import re
# from re import findall,search,S

secret_code = 'hadkfalifexxIxxfasdjifja134xxlovexx23345sdfxxyouxx8dfse'

'''
 .  : 匹配任意字符，换行符\n除外。。。几个点,匹配几次
 *  ：匹配前一个字符0次或无限次。。。 一直匹配,直到下一次匹配开始
 ?  ：匹配前一个字符0次或1次。。。    匹配
 .* ：贪心算法  匹配所有满足模型的字符串。返回字符串
 .*?：非贪心算法 仅仅匹配和模型一样的内容。返回列表
（） ：括号内的数据作为结果返回


findall：匹配所有符合规律的内容，返回包含结果的列表
Search： 匹配并提取第一个符合规律的内容，返回一个正则表达式对象（object)
Sub：    替换符合规律的内容，返回替换后的值


'''
# 1、.的使用
a = 'xyxy123A45600A00'
b1 = re.findall('.A..', a)
# 1、,后面要有空格,否则报弱警告。 2、#注释距离前边的代码2个空格以上距离,否则若警报 3、#后边要有一个空格,否则弱警告 4、#必须放在行首
# print b1
# ['3A45', '0A00'] 获取所有满足条件的结果。.代表一个元素。

# 2、*的使用
a = 'x1x1234xxxx'
b = re.findall('x*', a)
#  找出x的位置,其余没有的用''空替代
#  匹配前一个字符0次或无限次 一直匹配,直到下一个匹配开始
# print b

# 3、?的使用
a = 'xy0x1231xy0x2xyx'
# 依次匹配xyx,其中有y则匹配,无则不显示
b = re.findall('xy?x', a)
# 依次匹配xy,有y显示y,无则单显示x
b1 = re.findall('xy?', a)
# 依次匹配,有则显示y,无则显示""
b2 = re.findall('y?', a)
#  ?  ：匹配前一个字符0次或1次.匹配xy,y要么出现1次,要么不出现。
print (b)
print b1
print b2

print "222"*4

b = re.findall('xx.*xx',secret_code)
print b
b = re.findall('xx.*?xx',secret_code)
print b


print "222"*4

##########   掌握组合方式 .*?
b = re.findall('xx.*xx', secret_code)
print b
# 匹配xx xx之间内容, .任意匹配 *匹配不限次数 ?xx之间有就显示,无就不显示
c = re.findall('xx.*?xx', secret_code)
print c


##########   使用括号仅匹配()里面的
d = re.findall('xx(.*?)xx', secret_code)
print d
s = '''sdf  xxhello
# xxfsdf xxworldxxasdf'''
# 有换行,必须使用如下的方法:
e = re.findall('xx(.*?)xx',s,re.S)
# 换行符同时也被匹配进去
print e



# 对比findall与search区别
s2 = 'asdfxxIxx123xxlovexxdfd'
f = re.search('xx(.*?)xx123xx(.*?)xx',s2).group(0)
print f
print "1"*10
f2 = re.findall('xx(.*?)xx123xx(.*?)xx',s2)
print f2
print "1"*10
print f2[0][1]
print "1"*10


#sub的使用举例   替换
s = 'aaaaaa123rrrrr89999999'
output = re.sub('123(.*?)89','ABC%dDEF'%4567, s)
print output



#演示不同的导入方法
info = re.findall('xx(.*?)xx',secret_code,re.S)
for each in info:
    print each


#不要使用compile
pattern = 'xx(.*?)xx'
new_pattern = re.compile(pattern,re.S)
output = re.findall(new_pattern,secret_code)
print output


# 匹配数字\d+
a = 'asd00fasf1234567fasd555fas'
b = re.findall('(\d+)',a)
print b

a = ''''<td width="7%" align="center"><span class="red">0.01%</span></td>
<td width="5%" align="center"><span class="red">0.34%</span></td>
<td width="5%" align="center"><span class="red">0.80%</span></td>
<td width="5%" align="center"><span class="red">0.86%</span></td>'''
b = re.findall('<td width="5%" align="center"><span class="red">(.*?)</span></td>',a)[0]
print b




