#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-01

import sys
sys.path.append("/home/mysql1/anqu/python/code")
reload(sys)
import config
sys.setdefaultencoding('utf-8')

import cluster_k_means
import selectWord
import time

#对聚类处理合并或拆分
class combine_cluster():
	#初始化
	def __init__(self):
		# self.cluster_resault 
		pass

	#获取聚类结果
	def getData(self):
		K_means_cluster = cluster_k_means.Cluster_K_Means()
		selectWord.selectWord().writerObj(K_means_cluster.getClusterResault(),"cluster_resault.txt")
		# return K_means_cluster.getClusterResault()

	#按照数据集大小排序
	def arrange(self,cluster_resault):
		# cluster_resault = selectWord.selectWord().readObj("cluster_resault.txt")
		arrange_resault = []
		for Cluster in cluster_resault.keys():
			arrange_resault.append(cluster_resault.get(Cluster))
		#sort 
		for i in xrange(len(arrange_resault)-1):
			for re in xrange(i,len(arrange_resault)):
				if len(arrange_resault[i]) < len(arrange_resault[re]):
					arrange_resault[i],arrange_resault[re] = arrange_resault[re],arrange_resault[i]
		return arrange_resault

	#sort cluster resault by set size
	def sort(self,cluster_resault):
		sort_list = []
		for resault in cluster_resault.keys():
			sort_list.append((resault,len(cluster_resault.get(resault))))
			# print (resault,len(cluster_resault.get(resault)))

		#
		for i in xrange(len(sort_list)):
			for j in xrange(i,len(sort_list)):
				if sort_list[i][1] < sort_list[j][1]:
					sort_list[i],sort_list[j] = sort_list[j],sort_list[i]
		return sort_list

	#合并聚类到维度里
	def combine_cluster(self,sort_list,num=4):
		sta = False
		count = 0
		combine_cluster_re = []
		if len(sort_list) < num:
			num = len(sort_list)
		print len(sort_list)
		for sort in sort_list:
			if count < num:
				resault = []
				resault.append(sort[0])
				combine_cluster_re.append(resault)
			else:
				sc = count / num 
				sr = count % num
				if sc % 2 == 0:
					combine_cluster_re[sr].append(sort[0])
				else:
					combine_cluster_re[num-sr-1].append(sort[0])
			count += 1
		return combine_cluster_re

def main():
	Combine_Cluster = combine_cluster()
	# SelectWord = selectWord.selectWord()
	# cluster_resault = SelectWord.readObj("cluster_resault.txt")
	
	# sort_list = Combine_Cluster.sort(cluster_resault)
	# com_resault = Combine_Cluster.combine_cluster(sort_list,5)
	# SelectWord.getBetterPriorityWord(com_resault,20)
	# SelectWord.getBetterClassWord(com_resault,20)
	

if __name__ == '__main__':
	main()
