#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-15

import sys
sys.path.append("/home/spark/anqu/python/code")
reload(sys)
import config
sys.setdefaultencoding('utf8') 
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
import data_deal
import time 
import mysql_op
import myself_cluster
import particeple
import wordStatic
import selectWord

class Cluster_K_Means():
	def __init__(self):
		pass

	def  getData(self):
		data_a = data_deal.data_deal()
		mat,wdic = data_a.getMatrix()
		Iddic = data_a.getIddic(wdic)
		return mat,Iddic

	#K-Means,返回聚类结果
	def cluster_k_means(self,mat,k=100):
		resualt = KMeans(n_clusters=k,random_state=200).fit_predict(mat)
		return resualt

	# mini batch K-Means 聚类 返回聚类结果
	def cluster_mini_k_means(self,mat,k=100):
		# print mat
		return MiniBatchKMeans(n_clusters=k,random_state=400,init_size=6000).fit_predict(mat)

	#聚类结果与词条映射
	def mapResault(self,resualt,Iddic):
		word_cluster_resault = {}
		length = len(resualt)
		for num in xrange(length):
			if word_cluster_resault.has_key(resualt[num]):
				word_cluster_resault.get(resualt[num]).append(Iddic.get(num))
			else:
				word_list = []
				word_list.append(Iddic.get(num))
				word_cluster_resault.setdefault(resualt[num],word_list)
		return word_cluster_resault

	#打印聚类分析结果
	def print_Resault(self,word_cluster_resault):
		for line  in word_cluster_resault.keys():
			print "class "+ str(line) + "  contain words : " 
			word_list = word_cluster_resault.get(line)
			count = 0
			for word in word_list:
				print word,"  : ",
				count += 1
				if count % 5 == 0:
					print ''
			print "\n\n\n"

	#将聚类分析结果写入文件
	def writer_to_LocalFile(self,word_cluster_resault,type=2):
		filepath = "/home/spark/anqu/analysisResault/"
		ISOTIMEFORMAT='%Y-%m-%d %X'
		dateTime =  time.strftime( ISOTIMEFORMAT, time.localtime())
		filename = "clusterResault"+dateTime+".txt"
		fp = open(filepath+filename,"a")
		if type == 1:
			fp.write('''//--------------------------------------------------------------------------------------------------------//
				    ----------------------------------------using k-means method-------------------------------------\
				   //---------------------------------------------------------------------------------------------------------//\n''')
		else:
			fp.write('''//--------------------------------------------------------------------------------------------------------//
				    -----------------------------------using mini-k-means method----------------------------------\
				   //---------------------------------------------------------------------------------------------------------//\n''')
		particepleW = particeple.participle()
		word_static = wordStatic.wordStatic()
		for line in word_cluster_resault.keys():
			word_list = word_cluster_resault.get(line)
			word_an_re = particepleW.participleCluster(word_list)
			Describe_words = word_static.getStaticResault(word_an_re)
			writer_context = "class   "+ str(line) + " \nObject includes : "
			for Dws in Describe_words:
				writer_context += Dws + "  "
			writer_context += " \ncontain words : \n"
			fp.write(writer_context)
			word_list = word_cluster_resault.get(line)
			count = 0
			for word in word_list:
				fp.write(word+"  ; ")
				count += 1
				if count % 5 == 0:
					fp.write("\n")
			fp.write("\n\n\n\n")#k-means : 1 ;mini-k-means : 2

	#聚类分析结果写入数据库
	def write_to_sql(self,word_cluster_resault):
		print 'start.......'
		mysql = mysql_op.mysql_op("127.0.0.1","root","root","mysql")
		mysql.excute("create table if not exists cluster_resault (class_num int,words text)")
		mysql.excute("delete from cluster_resault")

		particepleW = particeple.particeple()
		for line in word_cluster_resault.keys():
			data = ""
			word_list = word_cluster_resault.get(line)
			for word in word_list:
				data += word+" , "
			sql = "insert into cluster_resault values(%d,%s)"%(line,data)
			print sql
			mysql.excute(sql)
			
	def run(self):
		clusterk_means = Cluster_K_Means()
		Matrix,Iddic = clusterk_means.getData()

		# k-means method
		# resualt = clusterk_means.cluster_k_means(Matrix)
		# word_cluster_resault = clusterk_means.mapResault(resualt,Iddic)
		# clusterk_means.writer_to_LocalFile(word_cluster_resault,1)

		# # mini k-means method
		# secResault = clusterk_means.cluster_mini_k_means(Matrix)
		# word_cluster_resault = clusterk_means.mapResault(secResault,Iddic)
		# clusterk_means.writer_to_LocalFile(word_cluster_resault)
		
		# # fuzzy self-organizing map Neural Network method
		# cla_num,resualt = myself_cluster.m_cluster_Som().cluster(Matrix)
		# word_cluster_resault = clusterk_means.mapResault(resualt,Iddic)
		# clusterk_means.writer_to_LocalFile(word_cluster_resault)
		# print "get classfacation : ",cla_num

	#获取聚类结果
	def getClusterResault(self):
		Matrix,Iddic = self.getData()
		resualt = self.cluster_k_means(Matrix)
		word_cluster_resault = self.mapResault(resualt,Iddic)
		return word_cluster_resault

def main():
	clusterk_means = Cluster_K_Means()
	# Matrix,Iddic = clusterk_means.getData()
	# print len(Matrix)
	# # k-means method
	# resualt = clusterk_means.cluster_k_means(Matrix)
	# word_cluster_resault = clusterk_means.mapResault(resualt,Iddic)
	# clusterk_means.writer_to_LocalFile(word_cluster_resault,1)

	# # mini k-means method
	# secResault = clusterk_means.cluster_mini_k_means(Matrix)
	# word_cluster_resault = clusterk_means.mapResault(secResault,Iddic)
	# clusterk_means.writer_to_LocalFile(word_cluster_resault)
	
	# # fuzzy self-organizing map Neural Network method
	# cla_num,resualt = myself_cluster.m_cluster_Som().cluster(Matrix)
	# word_cluster_resault = clusterk_means.mapResault(resualt,Iddic)
	# clusterk_means.writer_to_LocalFile(word_cluster_resault)
	# print "get classfacation : ",cla_num

	# #SOM自适应算法结果
	# resualt = selectWord.selectWord().readObj("Som_resault.txt")
	# # print len(resualt)
	# print len(set(resualt))
	# word_cluster_resault = clusterk_means.mapResault(resualt,Iddic)
	# clusterk_means.writer_to_LocalFile(word_cluster_resault)

if __name__ == '__main__':
	main()