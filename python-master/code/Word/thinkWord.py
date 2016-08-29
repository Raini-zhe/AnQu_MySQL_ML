#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-06
# 关键词的联想词的分析获取

import sys
sys.path.append("/home/mysql1/anqu/python/code")
reload(sys)
import config
sys.setdefaultencoding('utf-8')

from mysql_op import mysql_op
from particeple import participle
from data_deal import data_deal
from chinese import chinese

class thinkWord():
	def __init__(self):
		self.data = data_deal()
		self.mysql = mysql_op()

	#获取当前词的联想词集合
	def getThinkWord(self,word):
		mysql = mysql_op()
		chi = chinese()
		if chi.is_contains(word):
			sql = 'select word from hintWord where hintword=\"%s\"'%word
		else:
			sql = 'select word from hintWord where hintword=\'%s\''%word
		resault = mysql.select(sql)
		return resault

	#当前聚类下的联想词的获得 chinese 
	def getThinkWordCluster_ch(self,cluster_Words):
		thinkWords = []
		mysql = mysql_op()
		sql = 'select word,hintword from %s'%config.hintWord
		All_thinkwords = mysql.getWordPriority(sql)
		chi = chinese()
		for word in All_thinkwords:
			if word[1] in cluster_Words and chi.is_chinese(word[0]):
				thinkWords.append(word[0])
		return thinkWords

	#当前聚类下的联想词的获得 english
	def getThinkWordCluster_en(self,cluster_Words):
		thinkWords = []
		mysql = mysql_op()
		sql = 'select word,hintword from %s'%config.hintWord
		All_thinkwords = mysql.getWordPriority(sql)
		chi = chinese()
		for word in All_thinkwords:
			if word[1] in cluster_Words and chi.is_english(word[0]):
				thinkWords.append(word[0])
		return thinkWords
	#获取联想词的词热等信息数据
	

	#处理聚类后品类词记录
	def getParticepleWord(self,Datas):
		clusterS = []
		for data in Datas:
			cluster_Words = []
			for word in data:
				cluster_Words.append(word[0])
			clusterS.append(cluster_Words)
		return clusterS
def main():
	tWord = thinkWord()
	# re = tWord.getThinkWord('微信')
	# re = tWord.getThinkWordCluster(['微信',])
	# print re[0]

if __name__ == '__main__':
	main()