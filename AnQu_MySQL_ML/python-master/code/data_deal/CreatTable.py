#encodig=utf8mb4
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-11

import MySQLdb
import sys
sys.path.append("/home/spark/anqu/python/code/Tools")
sys.path.append("/home/spark/anqu/python/code/data_deal")
reload(sys)
sys.setdefaultencoding("utf8") 

from mysql_op import mysql_op
import MySQLdb

class CreateNewTable():
	def __init__(self):
		self.mysql = mysql_op()
		self.conn = MySQLdb.connect(host='localhost',user='root',passwd='root',db='mysql',port=3306,charset='utf8')
		self.cur = self.conn.cursor()

	def mapAppId(self):
		appIds = self.mysql.select('select searchApp from searchApp')
		for appId in appIds:
			pass