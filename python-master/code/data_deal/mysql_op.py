#encodig=utf8mb4
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-14

import sys
sys.path.append("/home/mysql1/anqu/python/code")
reload(sys)
import config
sys.setdefaultencoding("utf8") 
import chinese
import MySQLdb
import time

class mysql_op():
	def __init__(self,host = config.Host_IP,user=config.dataBase_user,passwd = config.dataBase_passwd,database=config.dataBase):
		try :
			self.conn = MySQLdb.connect(host = host,user=user,passwd=passwd,db = database,port=3306,charset='utf8')
			self.cur =  self.conn.cursor()
		except MySQLdb.Error ,e:
			print "Mysql connect Error   %d:  %s"%(e.args[0],e.args[1])

	def  is_contains(self,line):
		if line[0].contain("\'"):
			return "insert into ansearchApp values(\"%s\",%d,%d,%d)"%line
		else :
			return "insert into ansearchApp values(\"%s\",%d,%d,%d)"%line

	#过滤searchApp表中的非汉语词
	def selectA(self):
		resault = self.cur.execute("select word,priority ,searchCount  ,genre ,type,time from searchApp")
		# data = self.cur.fetchall()
		# self.cur.execute("delete from ansearchApp")
		data_l = []
		count = 0
		chin = chinese.chinese()
		#创建ansearchApp表
		#create table ansearchApp(word varchar(255),priority int,searchCount int ,genre varchar(255),type int,time int);
		anS_conn = MySQLdb.connect(host = config.Host_IP,user=config.dataBase_user,passwd=config.dataBase_passwd,db = config.dataBase,port=config.dataBase_port,charset='utf8')
		anS_cur = anS_conn.cursor()
		# print self.cur.rowcount
		word = {}
		for i in  xrange(self.cur.rowcount):#self.cur.fetchall():
			line = self.cur.fetchone()
			if line[0] in word:
				continue
			word.setdefault(line[0])
			if chin.is_chinese(line[0]) :
				data_l.append(line)
				if chin.is_contains(line[0]):
					sql = "insert into ansearchApp values(\"%s\",%d,%d,\'%s\',%d,%d)"%line
				else : 
					sql = "insert into ansearchApp values(\'%s\',%d,%d,\'%s\',%d,%d)"%line
				# print sql
				anS_cur.execute(sql)
				anS_conn.commit()
				# break

	#judge word is english
	def select_E(self):
		resault = self.cur.execute("select count(*) from searchApp")
		chin = chinese.chinese()
		data_len = self.cur.fetchone()[0]
		print data_len
		anS_conn = MySQLdb.connect(host = config.Host_IP,user=config.dataBase_user,passwd=config.dataBase_passwd,db = config.dataBase,port=config.dataBase_port,charset='utf8')
		anS_cur = anS_conn.cursor()
		for i in xrange(data_len/10000 + 1):
			resault = self.cur.execute('select word,priority ,searchCount  ,genre ,type,time from searchApp limit %d,10000'%(i*10000))
			data = list(self.cur.fetchall())
			insertData = []
			for word in data:
				sta = True
				for w in word[0].split(' '):
					if w.isalpha() == False:
						sta = False
						break
				if sta :	
					sql = ''
					if chin.is_contains(word[0]):
						sql = "insert into ansearchApp values(\"%s\",%d,%d,\'%s\',%d,%d)"%word
					else : 
						sql = "insert into ansearchApp values(\'%s\',%d,%d,\'%s\',%d,%d)"%word
					print sql
					anS_cur.execute(sql)
					anS_cur.execute(sql)
					anS_conn.commit()
					# time.sleep(10)
			# data = tuple(data)
			# print data[0]
			# sql = "insert into ansearchApp values(%s,%d,%d,%s,%d,%d)"
			# anS_cur.executemany(sql,tuple(insertData))
			# anS_cur.execute(sql)
			# anS_conn.commit()

	def delete(self):
		try :
			resault = self.cur.execute("select word from searchApp")
			data = self.cur.fetchall()
			chin = chinese.chinese()
			for line in data:
				if chin.is_chinese(line[0]) == False:
					sql = "delete from searchApp where word = \""+line[0]+"\""
					print sql
					try :
						re = self.cur.execute(sql)
						self.conn.commit()
					except MySQLdb.Error ,e :
						continue
		except MySQLdb.Error ,e:
			print "Mysql  execute error   %d  :  %s"%(e.args[0],e.args[1])

	def  select(self,select):
		try :
			resault = self.cur.execute(select)
			# print 'there has %s rows record ' % resault
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

	def excute(self,sql):
		resault = self.cur.execute(sql)
		self.conn.commit()

	def getWordPriority(self,sql):
		try :
			# sql = 'select priority from %s where type = 1'%table
			# print sql
			self.cur.execute(sql)
			data = self.cur.fetchall()
			data_l = []
			# print "there has %d rows record"%len(data)
		 	for line in data:
				data_l.append(line)
			return list(data_l)
		except MySQLdb.Error ,e :
			print "Mysql execute error %d : %s"%(e.args[0],e.args[1])

def main():
	mysql = mysql_op("127.0.0.1","root","root",config.dataBase)
	# data = mysql.getWordPriority("select  word,priority,searchCount from ansearchApp where type = 1 and genre like \"%6014%\"")
	# for line in data:
		# print line[0],line[1],line[2]
	# 数据去重，过滤速度慢
	if config.dataBase == config.database_chi:
		mysql.selectA()
	if config.dataBase == config.database_en:
		mysql.select_E()
	# print mysql.select('select word from ansearchApp limit 1')[0]
if __name__ == '__main__':
	main()



