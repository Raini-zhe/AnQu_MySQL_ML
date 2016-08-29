#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-16

import re

class chinese():
	def __init__(self):
		pass

	#判断是都包含中文
	def is_chinese(self,c_str):
		zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
		#一个小应用，判断一段文本中是否包含简体中：
		# contents=u'一个小应用，判断一段文本中是否包含简体中：'
		match = zhPattern.search(c_str)

		if match:
    			# print u'有中文：%s' % (match.group(0),)
    			return True
		else:
    			# print u'没有包含中文'
    			return False

	def is_english(self,words):
		for word in words.split(' '):
			if word.isalpha() == False:
				return False
		return True    			

    	#是否包含单引号
	def is_contains(self,c_str):
		an = re.compile(u'\'')
		match = an.search(c_str)
		if match:
			return True
		else:
			return False

def main():
	chin = chinese()
	str_1 = u'微信'
	str_2 = u'应用fashkjhdfshajfj fhdsjkahfdhak fdsa'
	print str_1,"is",chin.is_chinese(str_1)
	print str_2,"is",chin.is_chinese(str_2)

if __name__ == '__main__':
	main()