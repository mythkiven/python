# coding=utf-8


"""
模块:python中的模块,,就是工具类,封装了大量的共用函数

"""

# .pyc 文件
'''.pyc文件是指以.pyc为后缀名的这一类文件。
在执行Python模块的时候,有两种执行方 式:
一种是先将模块里面的内容编译成二进制语言,然后执行这些二进制语言,
另一种是直接执行对应模块的二进制语言程序。
第二种方式省略了编译这一步,所以 执行速度相对来说要快一些。
而把模块编译成二进制语言程序的这个过程叫做字节编译,这个过程会产生一个与编译的模块对应的.pyc文件。
编译的工作是由解释器来完成的!!所以python依然是解释型语言
.pyc文件就是经过编译后的模块对应的二进制文件


好处:
1、加快了模块的运行速度
2、同时pyc文件可以进行反编译的!!!

原理:
import 模块之后,第一次执行,如果没有pyc文件,会自动生成对应的模块pyc文件
'''
# sys模块 标准库模块  安装Python系统自带的
import sys  # 导入sys模块

print sys.version  # 版本
print sys.executable  # 当前运行的软件的地址
print sys.modules.keys()  # 当前导入模块的所有关键字

# 1、import
import math  # 导入模块,没有导入方法。

print math.pi

# 2、form....import
# 可以导入模块,同时引用属性或者方法
from sys import version  # 导入模块,同时导入指定的方法

print version  # 可以直接使用方法:因为已经导入了。

# 3、form....import*
# 可以导入模块,同时导入所有的属性方法
from math import *

print pi

########################################
# 主函数/模块:没有被别的函数/模块调用,只调用别的函数/模块
# 非主函数/模块:被调用的函数/模块
# 模块是不是主模块,主要看执行的方式
########################################

# __name__属性
# 如果一个模块的__name__属性的值是__main__,那么该模块是主模块,否则为非主模块
print __name__  # 看出这里是main值。
import sd_lib  # 导入sd__lib,然后run,可以看出,sd是非主模块。

print  sd_lib.add(1, 900)

# 如何保存为模块???




#######################################
# dir 函数 查看模块的功能:属性
import sys

print  dir(sys)  # 查看功能列表
# ['__displayhook__', '__doc__', '__excepthook__', '__name__', '__package__', '__stderr__', '__stdin__', '__stdout__', '_clear_type_cache', '_current_frames', '_getframe', 'api_version', 'argv', 'builtin_module_names', 'byteorder', 'call_tracing', 'callstats', 'copyright', 'displayhook', 'dont_write_bytecode', 'exc_clear', 'exc_info', 'exc_type', 'excepthook', 'exec_prefix', 'executable', 'exit', 'flags', 'float_info', 'getcheckinterval', 'getdefaultencoding', 'getdlopenflags', 'getfilesystemencoding', 'getprofile', 'getrecursionlimit', 'getrefcount', 'getsizeof', 'gettrace', 'hexversion', 'maxint', 'maxsize', 'maxunicode', 'meta_path', 'modules', 'path', 'path_hooks', 'path_importer_cache', 'platform', 'prefix', 'py3kwarning', 'setcheckinterval', 'setdlopenflags', 'setprofile', 'setrecursionlimit', 'settrace', 'stderr', 'stdin', 'stdout', 'subversion', 'version', 'version_info', 'warnoptions']
print  sys.__doc__  # 查看功能列表
print "\n\n"
c = []
print  dir(c)  # 这里是 列表属性
print  dir({})
print dir(())
