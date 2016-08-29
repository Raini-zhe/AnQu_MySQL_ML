#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-07

import sys
sys.path.append("/home/mysql1/anqu/python/code")
# sys.path.append("/home/mysql1/anqu/python/code/Tools")
reload(sys)
import config
sys.setdefaultencoding('utf8') 

import os
from mysql_op import mysql_op
# init 
# init database 
def init_mysql():
	mysql = mysql_op()
	# create table ansearchApp
	# create table ansearchApp(word varchar(255),priority int,searchCount int ,genre varchar(255),type int,time int);
	sql = 'create table if not exists ansearchApp(word varchar(255) CHARACTER SET utf8mb4,priority int,searchCount int ,genre varchar(255),type int,time int)'
	mysql.excute(sql)
	# create table 
	#create table wordSelectFeature (word varchar(255),priority int,searchCount int,relevancy float,cluster int);
	sql = 'create table if not exists wordSelectFeature (word varchar(255) CHARACTER SET utf8mb4,priority int,searchCount int,relevancy float,cluster int)'
	mysql.excute(sql)
	sql = 'create index searchAppWordIndex on searchApp(word)'
	mysql.excute(sql)

"""fileClassResaultPath = fileResaultPath + 'ClassResault'
fileKeyWordResaultPath = fileResaultPath + 'KeyWordResault'
fileObjectPath = fileResaultPath + "Object"
fileRootPath = '/home/mysql1/anqu/python/code/'        #config the path being the point your code was contained ! 
fileToolsPath = fileRootPath + "Tools"
fileWordsPath = fileRootPath+'Word'
fileAnalysisPath = fileRootPath+'analysis'
fileDataPath = fileRootPath + 'data_deal'
fileClusterPath = fileRootPath + 'Cluster'
fileWordAnalysisPath = fileRootPath + 'wordAnalysis'"""
# init file
def init_file():

	if os.path.exists(config.fileClassResaultPath) != True:
		os.mkdir(config.fileClassResaultPath)
	if os.path.exists(config.fileKeyWordResaultPath) != True:
		os.mkdir(config.fileKeyWordResaultPath)
	if os.path.exists(config.fileObjectPath) != True:
		os.mkdir(config.fileObjectPath)
	

def main():
	init_mysql()
	init_file()

if __name__ == '__main__':
	main()



