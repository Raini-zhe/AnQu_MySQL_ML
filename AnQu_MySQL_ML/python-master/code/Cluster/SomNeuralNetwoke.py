#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-29
# 功能 ：SOM自适应神经网络聚类算法实现，低效率是主要问题

import sys
sys.path.append("/home/mysql1/anqu/python/code")
reload(sys)
import config
sys.setdefaultencoding('utf8') 

import time
import mysql_op
import data_deal
import numpy as np
# import pandas as pd
import matplotlib as plot
from sklearn import preprocessing as preP
import math
import selectWord

#自适应神经网络聚类算法
class SomNeuralNetwork():
	#初始化
	def __init__(self,k_cluster=100, neighbor_radius = 1.0,learn_deep = 1.0):
		self.k_cluster = k_cluster
		self.neighbor_radius = neighbor_radius
		# self.cur_neighbor_radius = self.neighbor_radius
		self.learn_deep = learn_deep
		self.stop_deep_val = learn_deep / 100
		self.iter_times = 0
		self.Weight = preP.normalize(np.random.random((self.k_cluster,72)))

	#获取数据
	def getData(self):
		return data_deal.data_deal().getMatrix()

	#向量的归一化
	def NormalSize(self, Marix):
		return preP.normalize(Marix,'l2')

	#单个向量的归一化，
	def NormalSizeOne(self,Matrix,num):
		# line = Matrix[num] + self.learn_deep * (val - Matrix[num])
		Matrix[num,:] = preP.normalize([Matrix[num]],'l2')

	#更新邻域半径
	def updateNeighborRadius(self):
		self.neighbor_radius = self.neighbor_radius /math.e #* math.pow(math.e, -iter_times)

	#更新学习率
	def updateLearn_deep(self):
		self.learn_deep =  self.learn_deep / 2#math.pow(2,iter_times)

	#计算向量内积
	def calculInnerProduct(self,val,weight):
		return sum(map(lambda x,y:x*y,val,weight))

	#寻找点积最大的权值向量
	def findMaxWeight(self,val):
		Max_j = 0
		Max_innerProduct = self.calculInnerProduct(val,self.Weight[0])
		# print Max_innerProduct
		cur_innerProduct = 0
		for i in xrange(len(self.Weight)):
			cur_innerProduct = self.calculInnerProduct(val,self.Weight[i])
			if cur_innerProduct > Max_innerProduct:
				Max_j = i
		return Max_j

	#更新权值向量
	def updateWeight(self,val,Max_j):
		for wi in xrange(len(self.Weight)):
			inner_w = self.calculInnerProduct(self.Weight[wi],self.Weight[Max_j])
			if 2 - 2 * inner_w < self.neighbor_radius:
				arf = 1 - (2 - 2*inner_w)/self.neighbor_radius
				line = self.Weight[wi] + self.learn_deep * arf *(val - self.Weight[wi])
				self.Weight[wi,:] = preP.normalize([line],'l2')

	#训练数据，调整权重向量,自适应聚类
	def cluster(self,Matrix):
		resault_list = []
		print '样本数：',len(Matrix)
		print "阀值：",self.stop_deep_val
		print "strart ......"
		while self.learn_deep >= self.stop_deep_val:
			resault = []
			#迭代当前次，更新该次迭代下的权值向量
			for val in Matrix:
				index = self.findMaxWeight(val)
				resault.append(index)
				self.updateWeight(val,index)
			#更新相关的参数
			resault_list.append(resault)
			self.iter_times += 1
			self.updateNeighborRadius()
			self.updateLearn_deep()
		return resault_list[len(resault_list)-1]

	#非自适应的神经网络学习
	def unLearncluster(self,Matrix):
		resault_list = []
		print '样本数：',len(Matrix)
		print "阀值：",self.stop_deep_val
		print "strart ......"
		while self.learn_deep >= self.stop_deep_val:
			resault = []
			#迭代当前次，更新该次迭代下的权值向量
			for val in Matrix:
				index = self.findMaxWeight(val)
				resault.append(index)
				self.Weight[index,:] = preP.normalize([self.Weight[index]],'l2')
			#更新相关的参数
			resault_list.append(resault)
			self.iter_times += 1
			self.updateNeighborRadius()
			self.updateLearn_deep()
		return resault_list[len(resault_list)-1]

def main():
	Som = SomNeuralNetwork()
	# Matrix,wdic = Som.getData()
	# Som.findMaxWeight(Matrix[0])
	# resault = Som.unLearncluster(Matrix[0:2000])
	# print len(set(resault))
	# selectWord.selectWord().writerObj(resault,'Som_resault.txt')
	# resault = selectWord.selectWord().readObj('Som_resault.txt')
	# Som.NormalSizeOne(Matrix,0)

if __name__ == '__main__':
	main()
		