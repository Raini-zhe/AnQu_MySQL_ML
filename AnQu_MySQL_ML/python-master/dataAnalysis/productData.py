# product data
#writer : lgy
#datetime:2016-04-


import random

def productData():
	fp = open('testSet.txt','w')
	for i in range(100):
		X1 = random.randint(0,100)
		X2 = random.randint(0,100)
		lab = 0
		if X1 > X2:
			lab = 1
		fp.write(str(X1)+' '+str(X2)+' '+str(lab)+' '+'\n')
		# print i,X1,X2,lab
	fp.close()
	fp = open('dataSet.txt','w')
	for i in range(100):
		X1 = random.randint(0,100)
		X2 = random.randint(0,100)
		lab = 0
		if X1 > X2:
			lab = 1
		fp.write(str(X1)+' '+str(X2)+' '+str(lab)+' '+'\n')
		# print i,X1,X2,lab
	fp.close()

def ProductMatData(num):
	fp = open("dataMat.txt",'w')
	for i in range(num):
		link_num = random.randint(10,50)
		for num in range(link_num):
			s_j = random.randint(0,num)
			ij_v = 1.0/link_num
			fp.write(str(i)+' '+str(s_j)+' '+str(ij_v)+'\n')
	fp.close()


ProductMatData(500)

