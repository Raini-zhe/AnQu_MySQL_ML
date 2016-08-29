#-*- utf-8 -*-
# writer : lgy
# time :2015-10-23

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import zmq
import time
# import thread
from BuiltTopo import NetTopo
import sys 
sys.path.append('var')
from control import docker_operate
import traceback
import config 
import json
from thread_pool import ThreadPool

from docker import Client

#message compile 
def messageCompile(interval):
	operate = interval['operate']
	type_con = operate['type']
	print type_con
	if (type_con == 'create'):
		return 0
	elif type_con == 'delete':
		return 1
	else :
		return 2
		# return False
	
#deal thread
def deal(interval):
	topo = NetTopo()
	re = messageCompile(interval)
	if  re == 0:
		topo.del_switchs()
		resault = topo.buildNet_Topo(interval)
		if resault:
			docker = docker_operate()
			docker.resolve(interval)
	else:
		docker = docker_operate()
		docker.resolve(interval)
		if re == 1:
			topo.del_switchs()
	print interval


if __name__ == '__main__':
	client = zmq.Context()
	print 'Connect to server......'
	socket = client.socket(zmq.REQ)
	socket.connect("tcp://127.0.0.1:6662")
	dealThread = ThreadPool(3)
	while True:
		# get message
		socket.send("word")
		print 'listen......'
		message = socket.recv(102400)
		data = json.loads(message)

		# deal(data)
		dealThread.add_task(deal, data)
		# socket.send("word")
		# thread.start_new_thread(deal,(data,))





