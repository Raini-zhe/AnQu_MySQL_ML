#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-01

import sys
sys.path.append("/home/mysql1/anqu/python/code")
# sys.path.append("/home/mysql1/anqu/python/code/Tools")
reload(sys)
import config
sys.setdefaultencoding('utf8')

from cluster_k_means import Cluster_K_Means
import selectWord
import time
from data_deal import data_deal
from selectWord import selectWord
from calculSimilarity import similarity
from combine_cluster import combine_cluster
import os 
from mysql_op import mysql_op
from thinkWord import thinkWord
from particeple import participle

class clusterByCompleteObject():
	# init 
	def __init__(self,k = 100):
		self.cluster_k = k
		self.data = data_deal()
		self.cluster_Method = Cluster_K_Means()

	#获取基本的数据
	def getData(self,complete_ids):
		Matrix,wddic,word_list = self.data.getKeyWordDataByIds(complete_ids)
		Iddic = self.data.getIddic(wdic)
		return Matrix,Iddic,wdic,word_list

	#获取数据
	def analysis(self,Matrix,Iddic,wdic):
		if len(Matrix) <= self.cluster_k:
			self.cluster_k = len(Matrix) / 2
		resualt = self.cluster_Method.cluster_k_means(Matrix,self.cluster_k)
		cluster_resault = self.cluster_Method.mapResault(resualt,Iddic)
		# SelectWord = selectWord(cluster_resault,wdic)
		sim = similarity()
		similarity_re = sim.calSimilarityN(Matrix,cluster_resault,wdic)
		return resualt,similarity_re 

	#判断竞品关键ID是否相等
	def is_equals(self,com_ids,old_com_ids):
		if len(com_ids) != len(old_com_ids):
			return False
		od_len = len(old_com_ids)
		for c_id in com_ids:
			state = True
			i = 0
			while i < od_len:
				if old_com_ids[i] == c_id:
					break
				i += 1
			if i == od_len:
				return False
		return True

	# judge 
	def is_contains(self,com_ids,old_com_ids):
		pass

	#获取某一游戏的top K 竞品
	def getCompleteProductId(self,complete_Ids,top_k = 15):
		mysql = mysql_op()
		completeId_list = []
		sql = 'select topApp from topapp'
		topAppIds = mysql.select(sql)
		for complete_id in  complete_Ids:
			for appIds in topAppIds:
				appId = appIds.split(",")	
				# print appId
				if complete_id in appId:
					completeId_list += appId[0:top_k]+[complete_id]
					break
		# print completeId_list
		return list(set(completeId_list))

	#获得当前聚类相似度较高的前 top K 各聚类信息作为维度

	#测试代码
	def run(self,complete_Ids):
		select = selectWord()
		##提取竞品词从数据库
		# word_list = None
		if os.path.exists('/home/spark/anqu/analysisResault/Object/complete_Ids.txt') == False or self.is_equals(complete_Ids,select.readObj("complete_Ids.txt")) == False:
			# print '1'
			word_list = self.data.getDataByID(complete_Ids)
			# select.writeObj(word_list,"word_list.txt")
			#测试使用读取竞品词并将词的各属性列分离
			# word_list = select.readObj('word_list.txt')
			data = self.data.devide_data(word_list)
			words_ps = self.data.delRepeat(word_list)
			#得到分析计算矩阵，以及相关映射集合
			Matrix,wdic = self.data.calMatrix(data)
			Iddic = self.data.getIddic(wdic)
			# #计算聚类相似度
			resualt,similarity_re = self.analysis(Matrix,Iddic,wdic)
			#写入数据库
			if len(resualt) == len(words_ps) and len(resualt):
				print len(resualt)
				select.insert_data(words_ps,similarity_re,resualt)
			else:
				print "Error"
				print len(resualt),len(word_list),len(similarity_re)
			#获取聚类结果
			cluster_resault = self.cluster_Method.mapResault(resualt,Iddic)
			#写入聚类结果，避免下一次相同请求的重复计算
			select.writeObj(complete_Ids,"complete_Ids.txt")
			select.writeObj(cluster_resault,"cluster_resault.txt")
			return cluster_resault
		else:
			select.writeObj(complete_Ids,"complete_Ids.txt")
			cluster_resault = select.readObj("cluster_resault.txt")
			return cluster_resault

def main():
	k = 8
	# combine_num = 8
	# topWord = 100
	cluster = clusterByCompleteObject(k)
	complete_Ids = cluster.getCompleteProductId(['620112416',])
	print len(complete_Ids)
	# print complete_Ids
	# print complete_Ids
	# select = selectWord()
	# # complete_Ids = ('443354861','799406905','457517348','453640300','615187629','471802217','521922264','389801252','847334708','592331499','606080169','611129419','825355393','608188610','933456837','599534650')
	# # complete_Ids = ('890351673','708214926','685941739','671539572','645849323','658788107','652039347','880619256','664422011','695688524','743800927','632344249','903831702','576396994','894954694','820357891')
	
	# # # cluster_resault = select.readObj('cluster_resault.txt')
	# # # key_len = len(cluster_resault.keys())
	# # # print key_len
	# # # if len(cluster_resault.keys()) != k:	
	# cluster_resault = cluster.run(complete_Ids)
	# # select.writeObj(cluster_resault,'cluster_resault.txt')
	# # combine = combine_cluster()
	# # sort_list = combine.sort(cluster_resault)
	# # com_resault = combine.combine_cluster(sort_list,combine_num)
	# # select.getBetterPriorityWord(com_resault,30)
	# # select.getBetterClassWord(com_resault,30)

	# # select.getTopKKeyWord(topWord,combine_num)
	# clusterWord = select.getTopKClassWord(topWord,combine_num)
	# thinkword = thinkWord()
	# clusterWord = thinkword.getParticepleWord(clusterWord)
	# # print type(clusterWord[0])
	# # for cluster in clusterWord:
	# particiPle = participle(10)
	# staticWordCluster = particiPle.staticAllClusters(clusterWord)
	# for wordCluster in staticWordCluster:
	# 	for word in wordCluster:
	# 		print word[0],word[1]
	# 	print ''

if __name__ == '__main__':
	main()