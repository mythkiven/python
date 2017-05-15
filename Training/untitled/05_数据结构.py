# coding=utf-8

"""
做Python的内置数据结构,比如列表、元组等,而有 些数据组织方式,Python系统里面没有直接定义,
需要我们自己去定义实现这些数 据的组织方式,这些数据组织方式称为Python的扩展数据结构,比如栈、队列等。



"""



# 栈
"""
栈是一种数据结构。
不是内置数据结构,属于扩展数据结构。
这种数据结构具有这些特点:栈相当于一端开口一端封闭的容器,
把数据A移动到栈里面这个过程叫做进栈,也叫做压栈、入栈,数据A进入到栈里面之后,就到了栈顶,同时占了栈的一个位置。
当再进入一个数据B的时候,也就是再将一个数据入栈的时候,这个时候,新的数据就占据了栈顶的位置,
原来的数据就被新的数据压入到了栈顶的下一个位置里。栈只能对其栈顶的数据进行操作,
所以这个时候原来的数据就不能被操作,此时只能对新数 据进行操作,可以将其出栈或删除等。
等数据B出栈后,方可对A进行操作。


"""
#栈的实现

class Stack():     #定义栈 类
    def __init__(st,size):   #初始化的函数
        st.stack=[];         #本质是:列表
        st.size=size;        #设置传递的容量
        st.top=-1;           #设置栈顶的位置。当数据进入的时候,top就会不断的+,所以,栈最后是一个Y轴的柱子

    def push(st,content): #入栈的函数,将数据st压入栈。
        if st.Full():     #入栈前判断栈是都满了
            print "Stack is Full!"
        else:
            st.stack.append(content)#拼接内容
            st.top=st.top+1 #栈顶指针+1

    def out(st):            #出栈函数,将st压出栈。
        if st.Empty():      #出栈前 判断
            print "Stack is Empty!"
        else:
            st.top=st.top-1  #栈顶-1
    def Full(st):           #判断栈是否满的函数
        if  st.top==st.size:
            return True
        else:
            return False
    def Empty(st):          #判断栈是否空的函数
        if st.top==-1:
            return True
        else:
            return False


q = Stack(7)
print q.Empty()
q.push("hello")
print q.Empty()
q.out()
print q.Empty()
# 队列
"""
队列也是一种数据结构。
扩展的数据结构。
特点:队列相当于两端都开的容器,一端(队首)只能进行删除操作,不能进行插入操作,
而另一端(队尾)只能进行插入操作而不能进行删除操作,
数据是从队尾进------>>>队首出的。

"""


# 队列的实现
class Queue():
    def __init__(qu, size):#初始化
        qu.queue = [];#本质列表
        qu.size = size;
        qu.head = -1;
        qu.tail = -1;

    def Empty(qu):
        if qu.head == qu.tail:
            return True
        else:
            return False

    def Full(qu):
        if qu.tail - qu.head + 1 == qu.size:
            return True
        else:
            return False

    def enQueue(qu, content):
        if qu.Full():
            print "Queue is Full!"
        else:
            qu.queue.append(content)
            qu.tail = qu.tail + 1

    def outQueue(qu):
        if qu.Empty():
            print "Queue is Empty!"
        else:
            qu.head = qu.head + 1

        if 1:
            2
        elif 2:
            3



print "\n"
w=Queue(6)
print w.Empty()
w.enQueue("12")
print w.Empty()
w.outQueue()
print w.Empty()


