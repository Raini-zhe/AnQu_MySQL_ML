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

from mysql_op import mysql_op
from data_deal import data_deal
from thinkWord import thinkWord
from clusterByComleteObject import clusterByCompleteObject as cbco
from selectWord import selectWord
from cluster_k_means import Cluster_K_Means as CKM
from calculSimilarity import similarity
import numpy as np
from ClassWordExtend import ClassWordExtend as CWD
from SomNeuralNetwoke import SomNeuralNetwork as SNN
from NetLink import NetLink
import init
import time 

def getWord(keyWords):
	words = []
	for word in keyWords:
		words.append(word[0])
	return words

# run analysis chinese 
def runAnalysis_ch(Input_Ids,Cluster_K = 20,div = 20,TopKDiv = 50):
	ClusteBCO = cbco()
	cwd = CWD()
	data = data_deal()
	select  = selectWord()
	think = thinkWord()
	ckm = CKM()
	snn = SNN()
	netLink = NetLink()

	complete_Ids,genreIDs = netLink.getCompleteIds(Input_Ids)
	print 'com_Id',len(complete_Ids)
	# #real
	# st = time.time()
	st = time.time()
	keyWords = data.getDataByID_ch(complete_Ids)
	keyWords = data.delRepeatWord_ch(keyWords)
	# en_t = time.time()
	# print en_t - st
	select.writeObj(keyWords,"com_keyWords.txt")
	en = time.time()
	print '1 spend time:',en - st

	# #for test 
	# keyWords = select.readObj("com_keyWords.txt")

	print 'keyword',len(keyWords)
	# # # #get think words  获取联想词
	# # # #real
	st = time.time()
	thinkWords = think.getThinkWordCluster_ch(keyWords)
	select.writeObj(thinkWords,"thinkWords.txt")
	en = time.time()
	print '2 spend time :',en - st

	# thinkWords = select.readObj("thinkWords.txt")

	thinkWords = list(set(thinkWords))
	print 'thinkWords',len(thinkWords)

	st = time.time()
	# # #获取App 的类别下的关联词
	cwd_Words = cwd.getKeyWordofClassWord_ch(genreIDs)
	cwd_Words = list(set(cwd_Words))
	select.writeObj(cwd_Words,"cwd_Words.txt")
	en = time.time()
	# cwd_Words = select.readObj("cwd_Words.txt")
	print '3 spend time :',en - st
	print 'cwd_words',len(cwd_Words)

	all_Words = list(set(keyWords+thinkWords+cwd_Words))
	all_Words = data.delRepeatWord_ch(all_Words)
	select.writeObj(all_Words,"all_Words.txt")
	# all_Words = select.readObj("all_Words.txt")
	print 'all',len(all_Words)



	# # # #for test
	# # # #获取词的信息(词，词热，searchCount,genre)
	g_st = time.time()
	WordNews = data.getThinkWordPriorityAndSearchC(all_Words)
	WordNews = list(set(WordNews))	
	g_en = time.time()
	print '4 spent time : ',g_en - g_st
	select.writeObj(WordNews,"WordNews.txt")

	# WordNews  = select.readObj("WordNews.txt")
	print len(WordNews)

	# # # #cluster word 
	# # # # build matrix 
	st = time.time()
	Matrix = data.calMatrixByWordNews(WordNews)
	select.writeObj(Matrix,'Matrix.txt')
	# # # # cluster
	resualt = ckm.cluster_k_means(Matrix,Cluster_K)
	en = time.time()
	print 'cluster spend time :',en - st
	# # resualt = snn.cluster(Matrix)
	# # resualt = snn.unLearncluster(Matrix)

	print 'resault',len(Matrix),len(resualt)
	# # # 写入到数据库
	st = time.time()
	sim = np.zeros(len(resualt))	# all_Words = data.delRepeatWord(all_Words)
	select.insert_data(WordNews,sim,resualt)
	en = time.time()
	print 'insert into database spend time :',en - st
	# #提取分析结果
	select.getTopKKeyWord(TopKDiv,Cluster_K)
	select.getTopKTitleWord(TopKDiv,Cluster_K)

#run analysis english
def runAnalysis_en(Input_Ids,Cluster_K = 20,div = 20,TopKDiv = 50):
	ClusteBCO = cbco()
	cwd = CWD()
	data = data_deal()
	select  = selectWord()
	think = thinkWord()
	ckm = CKM()
	snn = SNN()
	netLink = NetLink()

	complete_Ids,genreIDs = netLink.getCompleteIds(Input_Ids)
	print len(complete_Ids)
	#real
	keyWords = data.getDataByID_ch(complete_Ids)
	# keyWords = data.delRepeatWord(keyWords)
	select.writeObj(keyWords,"com_keyWords.txt")

	#for test 
	# keyWords = select.readObj("com_keyWords.txt")

	print 'key',len(keyWords)
	# # #get think words  获取联想词
	# # #real
	thinkWords = think.getThinkWordCluster_en(keyWords)
	select.writeObj(thinkWords,"thinkWords.txt")

	# thinkWords = select.readObj("thinkWords.txt")

	print 'think',len(list(set(thinkWords)))

	# #获取App 的类别下的关联词
	cwd_Words = cwd.getKeyWordofClassWord_en(genreIDs)
	select.writeObj(cwd_Words,"cwd_Words.txt")

	# cwd_Words = select.readObj("cwd_Words.txt")

	print 'extend',len(cwd_Words)

	all_Words = list(set(keyWords+thinkWords+cwd_Words))
	all_Words = data.delRepeatWord_ch(all_Words)
	select.writeObj(all_Words,"all_Words.txt")

	# all_Words = select.readObj("all_Words.txt")
	# print 'all',len(all_Words)
	# all_Words = data.delRepeatWord_ch(all_Words)
	print 'all',len(all_Words)

	# # #for test
	# # #获取词的信息(词，词热，searchCount,genre)
	WordNews = data.getThinkWordPriorityAndSearchC(all_Words)
	WordNews = list(set(WordNews))	
	select.writeObj(WordNews,"WordNews.txt")

	# WordNews  = select.readObj("WordNews.txt")
	print 'news',len(WordNews)

	# # #cluster word 
	# # # build matrix 
	Matrix = data.calMatrixByWordNews(WordNews)
	# # # cluster
	resualt = ckm.cluster_k_means(Matrix,Cluster_K)
	# resualt = snn.cluster(Matrix)
	# resualt = snn.unLearncluster(Matrix)

	print 'resault',len(Matrix),len(resualt)
	# # 写入到数据库
	sim = np.zeros(len(resualt))	# all_Words = data.delRepeatWord(all_Words)
	select.insert_data(WordNews,sim,resualt)

	# #提取分析结果
	select.getTopKKeyWord(TopKDiv,Cluster_K)

def main():

	
	#input  parameters
	# Input_Ids = [994120614,1111594089,962734163]
	# Input_Ids = ['994120614','1111594089','962734163']
	# Input_Ids = ['882307119','834878585','685462046'] xiao xingxing
	# Input_Ids = ['791532221','834878585','882307119','1023663634','654897098']   #chinese
	# Input_Ids = ['692412579','945566094','553834731','479536744','916281743']
	# Input_Ids = ['1102362078','1065802303','1087318096','432278570','949933983']
	#Input_Ids = ['510582247','1106842267','689180123']
	Input_Ids = ['1111484111','1012852987','1083354212','1097663377']
	# genreIDs = ['6014','7014','6016','7008','7015','6024']
	# Input_Ids = ['998466140','639486670']
	Cluster_K = 20
	div = 20
	TopKDiv = 50

	#init 
	# init.init_mysql()
	# init.init_file()
	if config.dataBase == config.database_en:
		runAnalysis_en(Input_Ids,Cluster_K,div,TopKDiv)
	elif config.dataBase == config.database_chi:
		runAnalysis_ch(Input_Ids,Cluster_K,div,TopKDiv)
	elif config.dataBase == config.database_japan:
		pass



if __name__ == '__main__':
	main()
