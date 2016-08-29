#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-20

import sys
sys.path.append("/home/spark/anqu/python/code")
reload(sys)
import config
sys.setdefaultencoding('utf8') 
import numpy as np
import data_deal

class m_cluster_Som():
	def __init__(self):
		pass

	def And_sum(self,x,y):
		if x == y and x == 1:
			return 1
		return 0

	def  Or_sum(self,x,y):
		if x == 1 or y == 1:
			return 1
		return 0

	def Jaccard_dis(self,data_pro,data_lat):
		# print data_lat
		And_sum = sum(map(lambda x,y:self.And_sum(x,y),data_pro,data_lat))
		Or_sum = sum(map(lambda x,y:self.Or_sum(x,y),data_pro,data_lat))
		return float(And_sum)/float(Or_sum)

	def ave_distance(self,data,p_line):
		# print p_line
		dis_list = map(lambda x:self.Jaccard_dis(data,x),p_line)
		return sum(dis_list)/len(dis_list)

	def min_ave_distance(self,data,P_list):
		point = 0
		max_val = self.ave_distance(data,P_list[0])
		if len(P_list) == 1:
			return 1 - max_val,point
		for i in xrange(1,len(P_list)):
			cur_val = self.ave_distance(data,P_list[i])
			if cur_val > max_val:
				point = i
				min_val = cur_val
		return 1 - max_val,point

	def calcuGT(self,P_list):
		length = len(P_list)
		val = float(length)/250
		return 1 - (1- val * val) / (1 + 1 / float(length))

	def setClassification(self,P,data):
		for i in xrange(len(P)):
			if data[i] == 1:
				P[i] == 1

	def cal_ave_distance(self,p_line,data):
		return self.Jaccard_dis(p_line[0],data)

	def min_Dt(self,P_list,data):
		min_Dt = self.cal_ave_distance(P_list[0],data)
		point = 0
		for line in xrange(len(P_list)):
			cur_Dt = self.cal_ave_distance(P_list[line],data)
			if cur_Dt < min_Dt:
				point = line
				min_Dt = cur_Dt
		return min_Dt,point

	def cluster(self,mat,iter_times = 300,yibosilone = 0.01):
		P_list = []
		p = []
		p.append(mat[0])
		P_list.append(p)
		reault = []
		reault.append(1)
		count = 1
		for line in xrange(1,len(mat)):
			Dt , point= self.min_Dt(P_list,mat[line])
			Gt = self.calcuGT(P_list)
			if Dt > Gt:
				# print "first step"
				P = []
				P.append(mat[line])
				P_list.append(P)
				cla = len(P_list)
				reault.append(cla)
				self.setClassification(P_list[cla - 1],mat[line])
			else:
				# print "sec step"
				P_list[point].append(mat[line])
				P_list[point].append(mat[line])
				reault.append(point+1)
				# print P_list[point]
			count += 1
			if count % 500 == 0:
				print "finished ",count
		return len(P_list),reault

# def main():
	# my_cluster = m_cluster_Som()
	# mat = np.random.rand(4,5)
	# reault = my_cluster.cluster(mat)

	# def fit(self,):





