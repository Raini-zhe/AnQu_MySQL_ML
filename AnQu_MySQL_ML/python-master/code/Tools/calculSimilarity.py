#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-23

import sys
# sys.path.append("/home/spark/anqu/python/code/Cluster")
sys.path.append("/home/mysql1/anqu/python/code")
reload(sys)
import config
sys.setdefaultencoding('utf8') 

import myself_cluster as ms
import cluster_k_means
import data_deal 
from sklearn.cluster import MiniBatchKMeans as mbkm
import numpy as np
import time 

class similarity():
	def __init__(self):
		pass
	#初步的计算样本相似度的实现   10000条数据 处理37.2s
	def calSimilarity(self,Matrix,resault):
		re_length = len(resault)
		word_length = len(Matrix)
		if re_length != word_length:
			print "Error"
			return ;

		WordSimilarity = []
		s_time = time.time()
		for i in xrange(re_length):
			word_sum = 0
			word_count = 0
			for j in xrange(re_length):
				if  resault[i] == resault[j] :
					word_count += 1
					word_sum += ms.m_cluster_Som().Jaccard_dis(Matrix[i],Matrix[j])
			WordSimilarity.append((word_sum/word_count,resault[i]))
		e_time = time.time()
		print u"双层循环计算花费时间：",e_time - s_time
		return WordSimilarity
	#改进的计算样本相似度方法	 10000条数据 处理25.7 调高30%
	def calSimilarityL(self,Matrix,cluster_work_resault,wddic):
		re_length = len(Matrix)
		WordSimilarity = np.zeros(re_length)
		s_time = time.time()
		key_list = cluster_work_resault.keys()
		key_len = len(key_list)
		key_c = 0
		for cluster in key_list:
			print u"已完成百分%s"%((float(key_c)/float(key_len))*100)
			key_c += 1
			data = cluster_work_resault[cluster]
			num = len(data)
			for word in data:
				word_sum = 0
				Id = wddic.get(word)
				for word_l in data:
					Idl = wddic[word_l]
					word_sum += ms.m_cluster_Som().Jaccard_dis(Matrix[Id],Matrix[Idl])
				WordSimilarity[Id] = word_sum/num
		e_time = time.time()
		print "类簇内循环计算花费时间 :",e_time - s_time
		return WordSimilarity
	def calSimilarityN(self,Matrix,cluster_work_resault,wddic):
		re_length = len(Matrix)
		WordSimilarity = np.zeros(re_length)
		# min_sim = np.zeros((re_length,re_length)) - np.ones((re_length,re_length))
		# min_sim = {}
		# print min_sim
		s_time = time.time()
		key_list = cluster_work_resault.keys()
		key_len = len(key_list)
		key_c = 0
		for cluster in key_list:
			print u"已完成百分%s"%((float(key_c)/float(key_len))*100)
			key_c += 1
			data = cluster_work_resault[cluster]
			num = len(data)
			min_sim = {}
			for word in data:
				word_sum = 0
				Id = wddic.get(word)
				for word_l in data:
					Idl = wddic[word_l]
					val = 0.0
					#获取两个样本的相似度，已计算的不必再计算，未计算的并且一用到的，计算并存储
					if min_sim.has_key((Id,Idl)) or min_sim.has_key((Idl,Id)):
						if min_sim.has_key((Id,Idl)):
							val = min_sim.get((Id,Idl))
						else:
							val = min_sim.get(Idl,Id)
					else:
						val = ms.m_cluster_Som().Jaccard_dis(Matrix[Id],Matrix[Idl])
						min_sim.setdefault((Id,Idl),val)
					word_sum += val
				WordSimilarity[Id] = word_sum/num
		e_time = time.time()
		print "类簇内循环计算花费时间 :",e_time - s_time
		return WordSimilarity

	def run(self):
		data = data_deal.data_deal()
		Matrix,wddic = data.getMatrix()
		clusterk_means = cluster_k_means.Cluster_K_Means()
		Iddic = data.getIddic(wddic)

		resault = mbkm(n_clusters=200,random_state=400,init_size=6000).fit_predict(Matrix)
		# print len(Matrix)
		cluster_work_resault = clusterk_means.mapResault(resault,Iddic)
		print 'calcul.......'
		# WordSimilarity = self.calSimilarity(Matrix,resault)
		# WordSimilarity = self.calSimilarityL(Matrix,cluster_work_resault,wddic)
		WordSimilarity = self.calSimilarityN(Matrix,cluster_work_resault,wddic)
		# print len(WordSimilarity)
		# print len(resault)
		return WordSimilarity,resault

def main():
	sim = similarity()
	# print "start ......"
	# sim.run()
	# print 'finished!'


if __name__ == '__main__':
	main()
