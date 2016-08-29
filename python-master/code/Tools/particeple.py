#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-22

import sys
sys.path.append("/home/mysql1/anqu/python/code")
reload(sys)
import config
sys.setdefaultencoding('utf8') 
import jieba
from chinese import chinese

class participle():
	def __init__(self,top_K=10):
		self.top_K = top_K

	#句子分词
	def participleWord(self,sentence):
		sen = sentence.decode('utf-8')[0:8].encode('utf-8')
		return list(jieba.cut(sen,cut_all=False))

	#聚类结果分词
	def participleCluster(self,cluster_resaults):
		word_list = []
		for sentence in cluster_resaults:
			word_list.extend(self.participleWord(sentence))
		return word_list

	#数据分词统计  按字典的词出现次数统计结果排序（降序）
	def staticWord(self,word_list):
		wordStatic = {}
		for word in word_list:
			if word in wordStatic:
				val = wordStatic.get(word)
				wordStatic.pop(word)
				wordStatic.setdefault(word,val+1) 
			else:
				wordStatic.setdefault(word,1)
		for word in wordStatic.items():
			if chinese().is_chinese(word[0]) == False:
				wordStatic.pop(word[0])
		return sorted(wordStatic.iteritems(),key = lambda asd:asd[1],reverse=True)[0:self.top_K]

	#统计聚类各个簇的品类词
	def staticAllClusters(self,ClustersWords):
		static_resault = []
		for cluster in ClustersWords:
			word_list = self.participleCluster(cluster)
			resault = self.staticWord(word_list)
			static_resault.append(resault)
		return static_resault

def main():
	str_1 = '词的标签：每个词均有自己的genreID标签集合，根据标签的重要性可以确定词的重要性'
	participleW = participle()
	# words = participleW.participleWord(str_1)
	# resault = participleW.staticWord(words)
	# resaults = participleW.staticAllClusters(((str_1,),))
	# for resault in resaults:
	# 	for word in resault:
	# 		print word[0],word[1]
	# print str_1

if __name__ == '__main__':
	main()