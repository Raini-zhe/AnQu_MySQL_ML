#_*_ coding:utf-8 _*_
#writer : lgy
#datetime : 2016-04-26
from numpy import *
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression as LogReg

def loadDataSet(filename):
	dataMat = [];labelMat = []
	fr = open(filename)
	for line in fr.readlines():
		lineArr = line.strip().split()
		dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
		labelMat.append(int(lineArr[2]))
	return dataMat,labelMat

def sigmoid(inX):
	return 1.0 / (1 + exp(-inX))

#
def storgradAscent(dataMatIn,classLabels,numIter):
	dataMatrix = mat(dataMatIn)
	labelMatrix = mat(classLabels).transpose()
	m,n = shape(dataMatrix)
	alpha = 0.01
	weights = ones((n))
	print weights
	for j in range(numIter):
		# dataindex = range(m)
		for i in range(m):
			# alpha mei ci die dai shi xu yao tiao zheng
			# alpha = 4 / (1.0 + j + i) + 0.1
			# randIndex = int(random.uniform(0,len(dataindex)))
			# print dataMatrix[randIndex]
			h = sigmoid(sum(dataMatrix[i]*weights))
			error = classLabels[i] - h
			weights = weights + alpha * error * dataMatrix[i]
			print weights
			# del(dataindex[randIndex])
	# weights = list(set(weights))
	return weights

def gradAscent(dataMatIn,classLabels):
	# zhuan huan wei Numpy ju zhen shu ju lei xing
	dataMatrix = mat(dataMatIn)
	labelMatrix = mat(classLabels).transpose() 
	m,n = shape(dataMatrix)
	alpha = 0.001
	maxCycles = 500
	weights = ones((n,1))
	for k in range(maxCycles):
		#ju zhen xiang cheng
		h = sigmoid(dataMatrix*weights)
		error = (labelMatrix - h)
		weights = weights + alpha * dataMatrix.transpose() * error
		# print k,weights
	# classifier = LogReg()  # 使用类，参数全是默认的
	# classifier.fit(dataMatrix, labelMatrix)  # 训练数据来学习，不需要返回值
	# return classifier
	return weights

def predictData():
	dataMatIn,classLabels = loadDataSet('testSet.txt')
	dataMatrix = mat(dataMatIn)
	labelMatrix = mat(classLabels).transpose()
	classifier = LogReg()  # 使用类，参数全是默认的
	classifier.fit(dataMatrix, labelMatrix)  # 训练数据来学习，不需要返回值
	
	tdataMatIn,tclassLabels = loadDataSet('dataSet.txt')
	tdataMatrix = mat(tdataMatIn)
	tlabelMatrix = mat(tclassLabels).transpose()

	count = 0
	rCount = 0
	prCount = 0
	for i in range(0,len(dataMatIn)):
		res = classifier.predict(dataMatIn[i])
		if res == 1:
			count += 1
			if tclassLabels[i] == 1:
				prCount += 1
				rCount += 1
		else:
			if tclassLabels[i] == 1:
				rCount += 1
	return count,rCount,prCount	

def getPreSet(tlabelMatrix,lab):
	count = 0
	PreSet = []
	for i in range(0,len(lab)):
		# print int(lab[i]),int(labelMatrix[i])
		if int(lab[i]) == int(tlabelMatrix[i]):
			count += 1
			PreSet.append(tlabelMatrix[i])
	return PreSet,count

def plotBestFit(wei):
	weights = wei.getA()
	print weights
	dataMat,labelMat = loadDataSet('testSet.txt')
	dataArr = array(dataMat)
	n = shape(dataArr)[0]
	xcord1 = []; ycord1 = []
	xcord2 = []; ycord2 = []
	for i in range(n):
		if int(labelMat[i]) == 1:
			xcord1.append(dataArr[i,0])
			ycord1.append(dataArr[i,1])
		else :
			xcord2.append(dataArr[i,0])
			ycord2.append(dataArr[i,1])
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.scatter(xcord1,ycord1,s=10,c='red',marker='s')
	ax.scatter(xcord2,ycord2,s=10,c='green')
	x = arange(0.0,20.0,1)
	# print x 
	y = (- weights[0] - weights[1]*x)/weights[2]
	ax.plot(x,y)
	plt.xlabel('X1');plt.ylabel('X2')
	plt.show()

def main():
	P,R,PandR = predictData()
	print P,R,PandR
	Pre = float(PandR)/P
	Ref = float(PandR)/R
	F1 = Pre * Ref * 2 /(Pre + Ref)
	print "F1 : "+ str(F1) 

	dataMatIn,classLabels = loadDataSet('testSet.txt')
	# weights = gradAscent(dataMatIn,classLabels)
	weights = storgradAscent(dataMatIn,classLabels,150)
	plotBestFit(weights)
	
if __name__ == '__main__':
	main()

