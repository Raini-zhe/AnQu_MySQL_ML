import zmq
import time
import sys
sys.path.append('var')
import server
import json
from thread_pool import ThreadPool

def dealData():
	data


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:6662")
# thread = ThreadPool(4)

# while True:
print 'server .......'
# Wait for next request from client
print socket.recv()
# print "Received request: ", message
data = server.demo_create()
data1 = server.demo_create('ovs2.xml')
# data = server.demo_exec()
# data1 = server.demo_exec('')
# data = server.demo_del()
# data1 = server.demo_del('')
# print data

# Do some 'work'
# time.sleep (1) # Do some 'work'
# print '10'
# Send reply back to client
message = json.dumps(data)
socket.send(message)
print socket.recv()
message = json.dumps(data1)
socket.send(message)