#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-24

import sys
sys.path.append("/home/mysql1/anqu/python/code")
# sys.path.append("/home/mysql1/anqu/python/code/Tools")
reload(sys)
import config
sys.setdefaultencoding('utf8') 

import time
import mysql_op

class SelectWord():
	def __init__(self):
		self.mysql = mysql_op.mysql_op()

	#获取各类簇最大词热的word
	def selectMaxPriorityofCluster(self):
		max_priority = self.mysql.getWordPriority("select max(priority),cluster from wordSelectFeature group by cluster")
		max_prio_re = []
		# print max_priority
		for line in max_priority:
			sql = "select word,priority,max(searchCount),cluster from wordSelectFeature where priority = %d and cluster = %d"%line
			data = self.mysql.getWordPriority(sql)
			max_prio_re.append(data)
		return max_prio_re

	#获取当前词热前K大的word
	def selectTopKMaxPriority(self,K=5):
		sql = "select word,priority,searchCount,cluster from wordSelectFeature order by priority desc limit %d"%K
		# print sql
		max_priority_re = self.mysql.getWordPriority(sql)
		return max_priority_re

	#获取当前热词前K小的word
	def selectTopKMinPriority(self,K=5):
		sql = "select word,priority,searchCount,cluster from wordSelectFeature order by priority asc limit %d"%K
		min_priority_re = self.mysql.getWordPriority(sql)
		return min_priority_re

	# 获取当前各类簇的词热最小的word
	def selectMinPriorityofCluster(self):
		min_priority = self.mysql.getWordPriority("select min(priority),cluster from wordSelectFeature group by cluster")
		min_prio_re = []
		# print min_priority
		for line in min_priority:
			sql = "select word,priority,max(searchCount),cluster from wordSelectFeature where priority = %d and cluster = %d"%line
			data = self.mysql.getWordPriority(sql)
			min_prio_re.append(data)
		return min_prio_re

	# 获取当前词中的searchCount最大的Top K
	def selectTopKMaxSearchCount(self,K=5):
		sql = "select word,priority,searchCount,cluster from wordSelectFeature order by searchCount desc limit %d"%K
		# print sql
		max_searchCount_re = self.mysql.getWordPriority(sql)
		return max_searchCount_re

	#获取当前词中的searchCount最小的Top K 
	def selectTopKMinSearchCount(self,K=5):
		sql = "select word,priority,searchCount,cluster from wordSelectFeature order by searchCount asc limit %d"%K
		min_searchCount_re = self.mysql.getWordPriority(sql)
		return min_searchCount_re

	# 获取当前词中各类簇中searchCount最小的word
	def selectMinSerachCountOfCluster(self):
		min_searchCount_re = self.mysql.getWordPriority("select min(searchCount),cluster from wordSelectFeature group by cluster")
		min_searchCount_word = []
		for line in min_searchCount_re:
			sql = "select word,priority,searchCount,cluster from wordSelectFeature where searchCount = %d and cluster = %d"%line
			data = self.mysql.getWordPriority(sql)
			min_searchCount_word.append(data)
		return min_searchCount_word

	# 获取当前词中各类簇中searchCount最大的 word
	def selectMaxSearchCountOfCluster(self):
		max_searchCount_re = self.mysql.getWordPriority("select max(searchCount),cluster from wordSelectFeature group by cluster")
		# print 
		max_searchCount_word = []
		for line in max_searchCount_re:
			sql = "select word,max(priority),searchCount,cluster  from wordSelectFeature where searchCount = %d and cluster = %d"%line
			data = self.mysql.getWordPriority(sql)
			# print data[0]
			max_searchCount_word.append(data)
		return max_searchCount_word

	# 获取较大 的priority 和 searchCount较大的 Top K 结果
	def selectBigPriorityBigSearchCount(self,K=5):
		sql = 'create view word_view (word,priority,searchCount,cluster) as select word,priority,searchCount,cluster from wordSelectFeature order by priority desc,word limit 100'
		self.mysql.excute(sql)
		sql = 'select * from word_view order by searchCount desc ,word limit %d'%K
		BPBS_re = self.mysql.getWordPriority(sql)
		self.mysql.excute("drop view word_view")
		return BPBS_re

	# 获取较大priority 和较小的searchCount的Top K 查询结果
	def selectBigPrioritySmallSearchCount(self,K=5):
		sql = 'create view word_view (word,priority,searchCount,cluster) as select word,priority,searchCount,cluster from wordSelectFeature order by priority desc,word limit 100'
		self.mysql.excute(sql)
		sql = 'select * from word_view order by searchCount asc ,word limit %d'%K
		BPSS_re = self.mysql.getWordPriority(sql)
		self.mysql.excute("drop view word_view")
		return BPSS_re

	#获取较大的searchCount和较大的priority 的 Top K 查询结果
	def selectBigSearchCountBigpriority(self,K = 5):
		sql = "create view word_view (word,priority,searchCount,cluster) as select word,priority,searchCount,cluster from wordSelectFeature order by searchCount desc,word limit 100"
		self.mysql.excute(sql)
		sql = "select * from word_view order by priority desc ,word limit %d"%K
		BSBP_re = self.mysql.getWordPriority(sql)
		self.mysql.excute("drop view word_view")
		return BSBP_re

	#获取较大的searchCount和较小的priority的 Top K
	def selectBigSearchCountSmallPriority(self, K = 5):
		sql = "create view word_view (word,priority,searchCount,cluster) as select word,priority,searchCount,cluster from wordSelectFeature order by searchCount desc,word limit 100"
		self.mysql.excute(sql)
		sql = "select * from word_view order by priority asc ,word limit %d"%K
		BSSP_re = self.mysql.getWordPriority(sql)
		self.mysql.excute("drop view word_view")
		return BSSP_re

	def selectKeyWord(self,mainKeyWord):
		sql = "select cluster from wordSelectFeature where word = \'%s\'"%mainKeyWord
		resault = self.mysql.getWordPriority(sql)
		if len(resault) > 0:
			resault = resault[0][0]
			sql = "select word,priority,searchCount,cluster from wordSelectFeature where cluster = %d order by priority desc limit 15"%resault
			Key_word = self.mysql.getWordPriority(sql)
			for word in Key_word:
				print word[0],word[1],word[2],word[3]


	#将查询结果写入文件
	def write(self,fp,word_list):
		for words in word_list:
			for word in words:
				fp.write(word[0]+"  "+str(word[1])+ "   " +str(word[2]) +"  "+ str(word[3]) + "\n")
		fp.write("\n\n\n")

	#查询
	def find(self):
		filepath = "/home/spark/anqu/analysisResault/"
		ISOTIMEFORMAT='%Y-%m-%d %X'
		dateTime =  time.strftime( ISOTIMEFORMAT, time.localtime())
		filename = "selectWordResault"+dateTime+".txt"
		fp = open(filepath+filename,"a")
		fp.write(" -word-	-piority-		-searchCount-	-cluster-\n")

		fp.write("获取各类簇最大词热的word:\n")
		self.write(fp,self.selectMaxPriorityofCluster())

		fp.write("获取当前各类簇的词热最小的word:\n")
		self.write(fp,self.selectMinPriorityofCluster())

		fp.write("获取当前词中各类簇中searchCount最大的 word:\n")
		self.write(fp,self.selectMaxSearchCountOfCluster())

		fp.write('获取当前词中各类簇中searchCount最小的word:\n')
		self.write(fp,self.selectMinSerachCountOfCluster())

		fp.write("获取最小SearchCount的Top K 的word:\n")
		self.write(fp,[self.selectTopKMinSearchCount()])

		fp.write("获取最大searchCount的Top K 的word:\n")
		self.write(fp,[self.selectTopKMaxSearchCount()])

		fp.write("获取最小词热的Top K 的word:\n")
		self.write(fp,[self.selectTopKMinPriority()])

		fp.write('获取最大词热的Top K 的word:\n')
		self.write(fp,[self.selectTopKMaxPriority()])

		fp.write("获取较大 的priority 和 searchCount较大的 Top K 结果word:\n")
		self.write(fp,[self.selectBigPriorityBigSearchCount()])

		fp.write("获取较大 的priority 和 searchCount较小的 Top K 结果word:\n")
		self.write(fp,[self.selectBigPrioritySmallSearchCount()])

		fp.write("获取较大的searchCount和较大的priority 的 Top K 查询结果\n")
		self.write(fp,[self.selectBigSearchCountBigpriority()])

		fp.write('获取较大的searchCount和较小的priority 的 Top K 查询结果\n')
		self.write(fp,[self.selectBigSearchCountSmallPriority()])

def main():
	selectWord = SelectWord()
	# word_list = SelectWord.selectMinPriorityofCluster()
	# word_list = SelectWord.selectMaxPriorityofCluster()
	# word_list = SelectWord.selectMaxSearchCountOfCluster()
	# word_list = SelectWord.selectMinSerachCountOfCluster()

	# word_list = SelectWord.selectTopKMinSearchCount()
	# word_list = SelectWord.selectTopKMaxSearchCount(10)
	# word_list = SelectWord.selectTopKMinPriority(10)
	# word_list = SelectWord.selectTopKMaxPriority(10)

	# word_list = SelectWord.selectBigPriorityBigSearchCount()
	# word_list = [word_list]
	# for words in word_list:
	# 	for word in words:
	# 		print word[0],word[1],word[2],word[3]
	# SelectWord.find()
	# SelectWord.selectKeyWord("策略游戏")

if __name__ == '__main__':
	main()