#coding=utf-8

''' '''
'''
XPath 是一门语言
XPath可以在XML文档中查找信息
XPath支持HTML
XPath通过元素和属性进行导航
XPath可以用来提取信息
XPath比正则表达式厉害
XPath比正则表达式简单

'''
'''
安装lxml库
from lxml import etree
Selector = etree.HTML(网页源代码)
Selector.xpath(一段神奇的符号)
'''
'''
树状结构
逐层展开
逐层定位
寻找独立节点

手动分析法
Chrome生成法


'''
'''
语法:

//定位根节点
/往下层寻找
提取文本内容：/text()
提取属性内容: /@xxxx

nodename 	选取此节点的所有子节点。
/ 	从根节点选取。
// 	从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。
. 	选取当前节点。
.. 	选取当前节点的父节点。
@ 	选取属性。

* 	匹配任何元素节点。
@* 	匹配任何属性节点。
node() 	匹配任何类型的节点。

绝对位置路径：
/step/step/...

相对位置路径：
step/step/...

bookstore 	选取 bookstore 元素的所有子节点。
/bookstore

选取根元素 bookstore。

注释：假如路径起始于正斜杠( / )，则此路径始终代表到某元素的绝对路径！
bookstore/book 	选取属于 bookstore 的子元素的所有 book 元素。
//book 	选取所有 book 子元素，而不管它们在文档中的位置。
bookstore//book 	选择属于 bookstore 元素的后代的所有 book 元素，而不管它们位于 bookstore 之下的什么位置。
//@lang 	选取名为 lang 的所有属性。



1、以相同的字符开头
starts-with(@属性名称, 属性字符相同部分)
  <div id="test-1">需要的内容1</div>
  <div id="test-2">需要的内容2</div>
  <div id="testfault">需要的内容3</div>

2、标签套标签
string(.)
  <div id=“class3”>美女，
	  <font color=red>你的微信是多少？</font>
  </div>


'''
'''
Python并行化介绍
Map的使用
map 函数一手包办了序列操作、参数传递和结果保存等一系列的操作。
from multiprocessing.dummy import Pool
pool = Pool(4)
results = pool.map(爬取函数, 网址列表)

'''
'''
实战:
目标网站：http://tieba.baidu.com/p/3522395718
目标内容：跟帖用户名，跟帖内容，跟帖时间
涉及知识：
					Requests获取网页
					XPath提取内容
					map实现多线程爬虫

'''




from lxml import etree
html = '''
<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title>测试-常规用法</title>
    <a href="http://jikexueyuan.com1">极客学院1</a>
</head>
<body>
<div id="content">
    <ul id="useful">
      <a href="http://jikexueyuan.com2">极客学院2</a>
        <li>这是第一条信息</li>
        <li>这是第二条信息</li>
        <li>这是第三条信息</li>
    </ul>
    <ul id="useless">
        <li>不需要的信息1</li>
        <li>不需要的信息2</li>
        <li>不需要的信息3</li>
    </ul>

    <div id="url">
        <a href="http://jikexueyuan.com3">极客学院3</a>
        <a href="http://jikexueyuan.com/course/4" title="极客学院课程库">点我打开课程库</a>
    </div>
</div>
<div id="content">
    <ul id="useful">
        <a href="http://jikexueyuan.com5">极客学院4</a>
        <li>这是第一条信息2</li>
        <li>这是第二条信息2</li>
        <li>这是第三条信息2</li>
    </ul>
    <ul id="useless">
        <a href="http://jikexueyuan.com6">极客学院5</a>
        <li>不需要的信息12</li>
        <li>不需要的信息22</li>
        <li>不需要的信息32</li>
    </ul>

    <div id="url">
        <a href="http://jikexueyuan.com7">极客学院</a>
        <a href="http://jikexueyuan.com/course/8" title="极客学院课程库">点我打开课程库</a>
    </div>
</div>

</body>
</html>
'''

selector = etree.HTML(html)

#提取文本
content = selector.xpath('//ul[@id="useful"]/li/text()')
for each in content:
    print each

#提取属性
link = selector.xpath('//a/@href')
for each in link:
    print each

title = selector.xpath('//a/@title')
print title[0]





html1 = '''
<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
    <div id="test-1">需要的内容1</div>
    <div id="test-2">需要的内容2</div>
    <div id="testfault">需要的内容3</div>
</body>
</html>
'''

html2 = '''
<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
    <div id="test3">
        我左青龙，
        <span id="tiger">
            右白虎，
            <ul>上朱雀，
                <li>下玄武。</li>
            </ul>
            老牛在当中，
        </span>
        龙头在胸口。
    </div>
</body>
</html>
'''
print "\n\n\n"

selector = etree.HTML(html1)
content = selector.xpath('//div[starts-with(@id,"test")]/text()')
for each in content:
    print each

selector = etree.HTML(html2)
content_1 = selector.xpath('//div[@id="test3"]/text()')
for each in content_1:
    print each


data = selector.xpath('//div[@id="test3"]')[0]
info = data.xpath('string(.)')
content_2 = info.replace('\n','').replace(' ','')
print content_2


