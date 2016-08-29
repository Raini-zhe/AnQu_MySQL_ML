# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-14

import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8') 

class mysql_op():
	def __init__(self,host = 'localhost',user='root',passwd = 'root',database='mysql'):
		try :
			# print host
			self.conn = MySQLdb.connect(host = host,user=user,passwd=passwd,db = database,port=3306)
			self.cur =  self.conn.cursor()
			#print "connect success!"
		except MySQLdb.Error ,e:
			print "Mysql connect Error   %d:  %s"%(e.args[0],e.args[1])

	def  select(self,select):
		try :
			resault = self.cur.execute(select)
			print 'there has %s rows record ' % resault
			data = self.cur.fetchall()
			data_l = []
			for line in data:
				data_l.append(line[0])
			return list(data_l)
		except MySQLdb.Error ,e:
			print "Mysql  execute error   %d  :  %s"%(e.args[0],e.args[1])

	def insert(self,insert):
		try :
			resault = self.cur.execute(insert)
		except MySQLdb.Error ,e:
			print "mysql insert error  %d  : %s"%(e.args[0],e.args[1])




def main():
	mysql = mysql_op("192.168.5.154","root","root","mysql")
	print mysql.select("select genreID from _category order by genreID ")

if __name__ == '__main__':
	main()



