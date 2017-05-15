# coding=utf-8


# 函数的定义
# 格式
'''
def 函数名（）：
    函数内容;
'''


# 实例
def function1():
    a = 8
    print a


function1()


# 功能
# 1.实现取字符串长度的功能
'''
a="hellomyteacher"
print len(a)
'''

# 2.实现字符串的切割
# '''
a = "student"
b = a.split("u")
print b
# '''



# 1、形参实参

'''
a="abcdm"
print len(a)
'''
# 什么是形参
'''
def function1(a,b):
    if a>b:
        print a
    else:
        print b
   '''

# 什么是实参
'''
def function1(a,b):
    if a>b:
        print a
    else:
        print b
function1(1,3)
'''

# 参数的传递
# 第一中，最简单的传递
'''
def function(a,b):
    if a>b:
        print "前面这个数大于后面这个数"
    else:
        print "后面这个数比较大"
function(7,8)
'''


# 第二种，赋值传递
# '''
def function(a, b=8):
    print a
    print b


# function(1)
# function(1,2)
# '''


# 关键参数
def funct(a=1, b=6, c=7):
    print a
    print b
    print c


# funct(5)
# funct(b=7,a=8)
# funct(5,c=2,b=3)
# funct(b=4,c=2,a=1)

'''但是要注意，参数不能冲突'''


# funct(b=2,c=3,2)





# 2、全局局部变量
# 作用域
def func():
    i = 8


# print i
# print j
j = 9


# print j


# 局部变量
def func2(a):
    i = 7
    print i


i = 9


# func2(i)
# print i


# 全局变量  global
def func3():
    global iq
    iq = 7
    # print i


# i=9
func3()
iq = 9
print iq

# 3、使用、返回值
'''
函数的调用我们已经接触过了多次，要想调用一个函数，
在函数定以后，直接输一遍这个函数名即可，如果要传
递实参到函数里面执行，直接在调用的时候括号里面输
入实参即可。比如一个函数是def func3()：这样定
义的,那么我们调用它直接输入func3(参数)即可。其
中参数可以省略。
'''


def a():
    i = 1


a()

# 函数返回值
'''函数的返回值是通过return语句来实现的'''


# 一个返回值的情况
def test():
    i = 7
    return i


# print test()


# 多个返回值的情况
def test2(i, j):
    k = i * j
    return (i, j, k)


# x=test2(4,5)
# print x

y, z, m = test2(4, 5)
print y


# 4、python特有的文档字符串
# 用于打印函数内部的注释的文档。
# 如下:函数开头加入说明文档,后面用 print 函数.__doc__ 打印 或者help(函数) 打印

def d(i, j):
    '''这个函数实现一个乘法运算。

    函数会返回一个乘法运算的结果。'''
    k = i * j
    return k


print '直接打印:\n'
print d.__doc__

print "help方法打印:\n"
help(d)
