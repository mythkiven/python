#coding=utf-8


#控制流的类型
'''
控制流的类型有三种，
一种是顺序结构，
一种是分支结构，if
一种是循环结构 for while
'''

# if语句1
a=8;b=1
if a==8:
    print "1"
elif a!=9:
    print "2"
else:
    print "3"
# if语句2
if b==2:
    print "q"
else:
    print "w"
# if语句3
if b==a:
    print "yes"




# for语句

'''
for语句格式：
for i in 集合：
    执行该部分
else：
    执行该部分
'''

# for语句1
'''for i in [1,2,3,4,5]:
    print i
'''

# for语句2---range(a,b) 不含b
'''for i in range(1,5):
    print i #1\2\3\4
'''

# for语句2---range(a,b,c) ++c.每两个c执行一次
'''for i in range(1,10,3):
    print  i
'''

#最后看一个带嵌套的for语句

for i in range(1,10):
    if i%2==0:
        print i
        print "偶数"
    else:
        print i
        print "奇数"




# while
'''
while 条件为真：
    循环执行“该部分语句
    执行该部分语句
    执行该部分语句”
else：
    如果条件为假，执行该部分语句

#else部分可以省略
'''


#第一个是最简单没有else部分的
'''
a=True
while a:
    print "ABC"
'''

#第二个是有else部分的
'''
b=False
while b:
    print "ABC"
else:
    print "DEF"
'''

#第三个的有嵌套的while语句
a=1
while a<10:
    if a<=5:
        print a
    else:
        print "hello"
    a=a+1
else:
    print "test"


# break结束当前循环,结束循环,continue结束本次循环,跳入下次循环。





#continue
#continue语句的使用
'''
continue语句是放在循环语句中的，用来结束本次循环的语句。
'''
'''
a=1
while a<7:
    a=a+1
    if a==3:
        continue
    print a  #24567
'''
#continue语句在for循环中,结束本次循环
#程序a
'''
for i in range(1,7):
    if i==3:
        continue
    print i #12456
'''
#程序b
'''
for i in range(1,7):
    print i
    if i==3:
        continue #123456
 '''
#continue语句在双层循环语句中:结束本次条件的执行,仅本层,非外层的。
'''
a=1
while a<4:
    a=a+1;
    if a==3:
        continue
    print "3"
    for i in range(7,11):
        if i==9:
            continue
        print i#37810 37810
'''
#continue语句与break语句的区别
'''
continue语句指的是结束执行本次循环中剩余的语句，然后继续下一轮的循环。
而break语句指的是直接结束这个循环，包括结束执行该循环地剩余的所有次循环。
'''
#区分程序c和程序d

#程序c
'''
for i in range(10,19):
    if i==15:
        continue
    print i
'''
#程序d
'''
for i in range(100,109):
    if i==105:
        break
    print i
'''









# break语句
# break语句用法
'''
break语句是强制停止循环执行的意思，break语句用在循环语句中，出现break的地方将直接停止该循环地执行。
结束两层,上三层不结束

'''

# break语句用在while循环中
'''
a=1
while a:
    print a
    a=a+1
    if a==6:
        break
'''

# break语句在for循环中
'''
for i in range(5,9):
    print i
    if i>6:
        break
'''

# break语句在双层循环语句中
'''
a=10
while a<=12:
    a=a+1
    for i in range(1,4):
        print i
        if i==2:
            break#12 12 12
            # continue #123 123 123

'''

'''
a = 10
while a <= 12:
    a = a + 1
    for i in range(1, 7):
        print i
        if i == 5:
            break
    if a == 11:
        break
'''