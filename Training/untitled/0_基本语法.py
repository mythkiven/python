# coding=utf-8
# 默认不支持 utf8 需要加上注释: coding=utf-8

# 基本的数据类型:数、字符串
# 数据类型: 列表、元祖、集合、字典
##########################################################
# 1、数据类型5种:int long float bool(true false) complex(复数 2+3j)

##########################################################
# 2、字符串    '',"",'''  '''三引号字符串可以换行
print("It's'a dog!")   #双引号 可以包含单引号
# print("It's' "a" dog!")#双引号 不能包含双引号
# print('It's'a dog!')#单引号 不能包含单引号
print('It "a" dog!')#单引号可以包含双引号
sanyh = '''
aa
    bb
        ccc
        ccc
    bb
aa'''
# 三引号  可以保持格式
print (sanyh)
# 转义符 \可以在双引号或者单引号里面输出单双引号
print ('it\'s a dog ')
# 自然字符串 r 保留转义字符
print (r'it\'s a dog')
# 重复字符串,*5重复5次
print ("hello\n"*5)

# 子串
# 索引,下标
aa = "01234567bbcceeddff"
print ("索引法:从0开始:子串1: {0}".format(aa[1]))
print ("切片法:从1开会:子串0-2:{0}".format(aa[:2]))
print ("切片法:从1开始:子串2-7:{0}".format(aa[2:7]))

##########################################################
# 3、数据类型: 列表、元祖、集合、字典
print "\n\n3、数据类型: 列表、元祖、集合、字典"

# 3.1、列表 []
students = ["11","22","33"]
print students[0]
students[0]="111"
print students

# 3.2、元组 ()
studentsa = ("aa","bb","cc")
print studentsa[0]
# studentsa[0]="111" 不能修改元组数据
print studentsa

# 3.3、集合 set()元素唯一
sea = set("0122333444")
print sea#默认已经将重复的元素去除掉 et(['1', '0', '3', '2', '4'])
seb = set("550")
#交集 结果也是集合
print sea&seb
# 并集 可以去重复的
print sea|seb
# 差集
print sea-seb
# 去除重复的元素
new = set(sea)
print  new

# 3.3、字典
zidian = {"a0":sea,"a1":seb,"a3":new}
print zidian
# 添加项目
zidian["b1"]="bb"
print zidian

##########################################################
# 4、标识符 关键字28个
# and,elif,global,or,else,pas,break,continue,import, clas,return,for,while
# 大小写敏感


##########################################################
# 5、对象:  一切皆对象
print "\n\n 5、对象"
# 持久化数据: 需要先将数据序列化,然后存起来,然后再恢复成原来的数据,取出来
# 序列化的过程就是 pickle 腌制

import pickle #腌制

#dumps(object) 将对象序列化
lista = ["name","age"]
listb = pickle.dumps(lista)
print "序列化后:{0}".format(listb)

# loads(string)将对象/类型原样恢复,
listc=pickle.loads(listb)
print "恢复后:{0}".format(listc)

# dump(object,file)将对象序列化储存到文件里
group1 = ("nihao","wohao")
f1=file('1.pk1','wb')#write。用来写入的文件
pickle.dump(group1,f1,True)
f1.close()

# load(object,file)将dump()储存的文件的 数据恢复
f2 =file('1.pk1','rb')#read。用来读取的文件
t=pickle.load(f2)
f2.close()
print "文件恢复后:{0}".format(t)


##########################################################
#6、逻辑行与物理行
#以下是3个物理行
print "abc"
print "789"
print "777"

#以下是1个物理行，3个逻辑行。分号来区分
print "abc";print "789";print "777"

#以下是1个逻辑行，3个物理行
print '''这里是
由极客学院
提供的Python教程！'''


#6.1、分号使用规则

#所有的逻辑行后均应使用分号，但以下条件除外
print "123";print "456";
print "777";

#分号可以省略的条件是指：每个物理行的行末可以省略分号,当然也可以不省略分号。
print "123";print "456"  # 这里的分号可以省略，也可以不省略
print "777"              # 这里的分号可以省略，也可以不省略

#一般情况下，行首应该不留空白
import sys

#缩进的方法有两种，可以按空格，也可以按tab键


#if语句的缩进方法
a=7
if a>0:
    print "hello"

#while语句的缩进方法
a=0
while a<7:
    print a
    a+=1

##########################################################


# 变量
print "\n\n 99、变量"
a=22
b=18
c=-1
print (a*b)

# if判断语句

if a>b :
    print ("a>b-技术")
elif a>c :
    print ("a>c")
elif a<c :
    print ("a<c")
else:
    print ("判断语法结束")


# 循环语句
for i in range(0,10):
    print ("item{0},{1}".format(i,"hello"))
for i in range(0,10,2):#0到10循环,每次+2
    print ("item{0},{1}".format(i,"-----"))


# 函数
def sayhello():
    print ("hello")
sayhello()

def max(a,b):
    if a>b:
        return a
    else:
        return b
print (max(2,-1))


# 类
class Hello:
    def __init__(self,name):#构造方法
        self._name = name#属性

    def sayHello(self):#方法
        print ("Hello {0}".format(self._name))

class Hi(Hello):#继承
    def __init__(self,name):#个人的构造
        Hello.__init__(self,name)#首先执行 父类的构造方法

    def sayHi(self):
        print ("Hi{0}".format(self._name))

h = Hello("类")
h.sayHello()

h1=Hi("继承\n")
h1.sayHi()


# 引用外部的文件--方式1:
import sd_lib
hh = sd_lib.Hello()
hh.sayHello()

# 引用外部文件--方式2:
from sd_lib import Hello_Two
hh2 = Hello_Two()
hh2.doHello()

