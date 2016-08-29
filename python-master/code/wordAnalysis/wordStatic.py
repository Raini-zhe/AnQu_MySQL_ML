#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-22

import sys
sys.path.append("/home/spark1/python/")
sys.path.append("/home/spark/anqu/python/code/Tools")
reload(sys)
sys.setdefaultencoding('utf8') 
import jieba
import chinese

class wordStatic():
	def __init__(self):
		pass

	def wordStatic(self,cluster_resaults):
		word_count = {}
		chin = chinese.chinese()
		length = len(cluster_resaults)
		for word in cluster_resaults:
			if chin.is_chinese(word) == False or len(word) <= 1:
				continue
			if word_count.has_key(word):
				word_count[word] += 1
			else:
				word_count.setdefault(word,1)
		return word_count,length

	#词的合并：将字词合并为一个全词如：六边--->六边形
	def combine_subWord(self,sort_word):
		length = len(sort_word)
		Describe_Words = []
		if length == 0:
			return Describe_Words
		elif length == 1:
			return sort_word[0]
		else:
			pass
		for i in xrange(length-1):
			state = False
			for j in xrange(i+1,length):
				if sort_word[i][0] in sort_word[j][0]:
					state = True
				elif sort_word[j][0] in sort_word[i][0]:
					state = True
					sort_word[j][0] = sort_word[i][0]
				else:
					continue
			if state == False:
				Describe_Words.append(sort_word[i])
		Describe_Words.append(sort_word[length - 1])
		return Describe_Words

	#打印合并词的结果
	def printWord(self,word):
		for w in word:
			print w[0],
		print ''

	#
	def getWord(self,word_count,length,threshold_V= 0.008,word_num = 10):
		sort_re = sorted(word_count.iteritems(), key=lambda d:d[1], reverse = True)
		re = []
		val = length * threshold_V

		for sort_r in  sort_re:
			if sort_r[1] > val :
				re.append(sort_r[0])

		Describe_Words = self.combine_subWord(re)
		if len(Describe_Words) >= word_num:
			return Describe_Words[0:word_num]
		else:
			return Describe_Words

	def getStaticResault(self,cluster_resaults):
		word_count ,length= self.wordStatic(cluster_resaults)
		Dws = self.getWord(word_count,length)
		return Dws

# def combine_substr(word_list):
# 	# if len(word_list) <= 1:
# 		# return word_list:
# 	length = len(word_list)
# 	if length == 1:
# 		return word_list
# 	re = []
# 	for i in xrange(length-1):
# 		st = False
# 		for j in xrange(i+1,length):
# 			if word_list[i] in word_list[j]:
# 				st = True
# 		if st == False :
# 			re.append(word_list[i])
# 	re.append(word_list[length-1])
# 	return re
def main():
	word_static = wordStatic()
	#消除  罗斯  俄罗斯  消消  六边  七彩  六角  方块  六边形  游戏   
	word = [('消除',4),('罗斯',3),('俄罗斯',5),('六边',6),('六边形',7)]	
	word_static.printWord(word_static.combine_subWord(word))
	# word_list = ["消除", "罗斯","俄罗斯","消消","六边","七彩","六角","方块","六边形","游戏"]
	# word_static.printWord(combine_substr(word_list))

if __name__ == '__main__':
	main()
