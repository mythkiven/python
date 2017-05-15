# coding=utf-8
class Hello:
    def sayHello(self):
        print ("sd_lib:这是一个外部类\n")

class Hello_Two:
    def doHello(self):
        print ("sd_lib:zheshiyigewaibulei\n")

if __name__=="__main__":
    print "sd_lib是主模块"
else:
    print "sd_lib是非主模块"


def add(i,j):
    k=i+j
    return k

k=add(1,-1)
print k

