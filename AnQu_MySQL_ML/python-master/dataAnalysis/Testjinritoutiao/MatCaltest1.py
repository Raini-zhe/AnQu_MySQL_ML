#_*_ coding:utf-8 _*_
#writer : lgy
#datetime : 2016-05-04

from numpy import *
# from matplotlib.pyplot as plt
import time
def MatCal():
	startTime = time.time()
	endTime = time.time()
	C_time = []
	for j in range(20):
		randMat = mat(random.rand(500,500))
		randMatS = mat(random.rand(500,500))
		startTime = time.time()
		for i in range(50):
			randMatS = randMatS * randMat
			# print i
		# print randMatS
		endTime = time.time()
		C_time.append((endTime - startTime))
	# print C_time
	all_time = sum(C_time)
	# reduce(lambda x,y:x+y, C_time)
	count = len(C_time)
	print all_time / count

def main():
	MatCal()

if __name__ == '__main__':
	main()

