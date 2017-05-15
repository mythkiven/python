# coding=utf-8


# 文件写
f = open('test.txt','a')
for i in range(10):
    f.write('hello,')
    f.write('world!\n')
f.close()

#文件读

ff= open('test.txt','r')
d = ff.read(4)
print d