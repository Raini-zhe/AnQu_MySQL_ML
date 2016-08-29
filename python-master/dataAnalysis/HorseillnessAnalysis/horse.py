#_*_ coding:utf-8 _*_
#writer : lgy
#datetime : 2016-04-27
# analysis horse illness

from numpy import *
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression as LogReg
import random

def Loaddata(filename):
	dataMat = [];labMat = [];
	with open(filename,"r") as fp:
		line = fp.readline()
		while line != '' and len(line) > 10:
			datalist = line.split()
			data = []
			for i in range(len(datalist)-2):
				if datalist[i] != "?":
					data.append(float(datalist[i]))
				else:
					data.append(float(0))
			dataMat.append(data)
			if datalist[len(datalist)-1] == "?":
				labMat.append(float(random.randint(1,2)))
			else :
				labMat.append(float(datalist[len(datalist)-1]))
			line = fp.readline()
	return dataMat,labMat

def predictData(lfilename,pfilename):
	dataMat,labMat = Loaddata(lfilename)
	datamatrix = mat(dataMat)
	labMatrix = mat(labMat).transpose()

	classifier = LogReg() 
	classifier.fit(datamatrix,labMatrix)

	tdataMatIn,tclassLabels = Loaddata(pfilename)
	tdataMatrix = mat(tdataMatIn)
	tlabelMatrix = mat(tclassLabels).transpose()

	count = 0
	rCount = 0
	prCount = 0
	for i in range(0,len(tdataMatIn)):
		res = classifier.predict(tdataMatIn[i])
		if res == 1:
			count += 1
			if tclassLabels[i] == 1:
				prCount += 1
				rCount += 1
		else:
			if tclassLabels[i] == 1:
				rCount += 1
	return count,rCount,prCount	

def main():
	# Loaddata('horse_test.txt')
	
	P,R,PandR = predictData("horse_test.txt","horse_data.txt")
	print P,R,PandR
	Pre = float(PandR)/P
	Ref = float(PandR)/R
	F1 = Pre * Ref * 2 /(Pre + Ref)
	print "F1 : "+ str(F1) 

if __name__ == '__main__':
	main()
