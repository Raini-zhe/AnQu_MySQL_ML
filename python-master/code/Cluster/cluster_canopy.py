#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-15

import sys
sys.path.append("/home/spark/anqu/python/code")
reload(sys)
import config
sys.setdefaultencoding('utf8') 

import data_deal

def fun1(x,y):
	if x == y and x == 1:
		return 1
	return 0

def fun2(x,y):
	if x == 1 or y == 1:
		return 1
	return 0

def printf(x):
	if x < 0.2:
		print x

class canopy():
	def __init__(self):
		pass

	def jaccard(self,data,re):
		# print data
		And = sum(map(lambda x,y:fun1(x,y)  ,data[1],re[1]))
		Or = sum(map(lambda x,y:fun2(x,y),data[1],re[1]))
		return 1 - float(And)/float(Or)

	def calcuDistance(self,data,re,disType = 1):
		if disType == 1:
			# print "jaccard"
			return min(map(lambda x:self.jaccard(x,data),re))

		if disType == 2:
			# print 'cos dis'
			pass

		if disType == 3:
			# print 'Euclidean '
			pass

	def calcuShortDistance(self,data,re_list,disType = 1):
		if disType == 1:
			# print "jaccard"
			# print type(re_list[0][0])
			minP = 0
			minV = self.calcuDistance(data,re_list[0])
			for num in xrange(len(re_list)):

				cur = self.calcuDistance(data,re_list[num])
				if cur <= minV:
					minV = cur
					minP = num
			return minV,minP
			# return min(map(lambda x : self.calcuDistance(data,x) , re_list))

		if disType == 2:
			 #print "cos dis"
			 pass

		if disType == 3:
			#print 'Euclidean'
			pass

	def calcuCanopy(self,datalist,T1,T2):
		re_list = []
		print "T1 = %f,T2 = %f"%(T1,T2)
		count  = 0
		while len(datalist) != 0:
			res = []
			res .append(datalist[0])
			re_list.append(res)
			datalist.remove(datalist[0])
			if len(datalist) == 0:
				break
			for data in datalist:
				distance,point = self.calcuShortDistance(data,re_list)
				if distance < T2:
					# print 'a:%d'%point
					re_list[point].append(data)
					datalist.remove(data)
				elif  distance > T1:
					rest = []
					rest.append(data)
					re_list.append(rest)
					datalist.remove(data)
				# else:
					# print data
		return re_list

def main():
	cano = canopy()
	# data_d = data_deal.data_deal()
	# data = data_d.getDadic()
	# dataL = data[0:1000]
	# resault = cano.calcuCanopy(dataL,0.95,0.4)
	# print len(resault)

if __name__ == '__main__':
	main()