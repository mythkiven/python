#-*-coding:utf8-*-
from __future__ import print_function

sql = ('SELECT * from ipdata limit 10')

# mysql-connector
print('mysql-connector'.center(50, '='))
import mysql
import MySQLdb

import mysqldbda
conn = MySQLdb.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    passwd = 'jxc123',
    db = 'jijinku',
)
cur = conn.cursor()
# 插入数据
sqli="insert into student values(%s,%s,%s,%s)"
cur.execute(sqli,('3','Huhu','2 year 1 class','7'))

cur.close()
conn.commit()
conn.close()



# cnx = connector.Connect(host="pythontest.cgngr7chq0yp.ap-northeast-1.rds.amazonaws.com", user="jilu",
#                             password="123456", database="pythontest", charset="utf8")
# # cnx.autocommit = True
# db0 = cnx.cursor()
#
# db0.execute(sql)
# for row in db0:
#     print(*row) # print row[0], row[1], row[2], row[3]
#
#
# # MySQLdb
# print('MySQLdb'.center(50, '='))
# import MySQLdb
#
# def connect_mysql(db_host="pythontest.cgngr7chq0yp.ap-northeast-1.rds.amazonaws.com", user="jilu",
#                    passwd="123456",db="pythontest", charset="utf8"):
#     conn = MySQLdb.connect(host=db_host, user=user, passwd=passwd, db=db, charset=charset)
#     conn.autocommit(True)
#     return conn.cursor()
#
# db1 = connect_mysql()
# db1.execute(sql)
# for row in db1:
#     print(*row)
#
# # torndb1
# print('torndb1'.center(50, '='))
# import torndb
# import simplejson as json
#
# db2 = torndb.Connection(
#     host='pythontest.cgngr7chq0yp.ap-northeast-1.rds.amazonaws.com',
#     database='pythontest',
#     user='jilu',
#     password='123456',
#     charset="utf8")
# rows = db2.query(sql)
# for row in rows:
#     print(json.dumps(row, ensure_ascii=False))
#
# # # torndb2
# # print('torndb3'.center(50, '='))
# # row = db2.get(sql)
# # print(json.dumps(row, ensure_ascii=False))
# #
# # torndb3
# print('torndb2'.center(50, '='))
# row = db2.get('SELECT * from ipdata limit 1')
# print(json.dumps(row, ensure_ascii=False))



