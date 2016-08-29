#-*- utf-8 -*-
# writer : lgy
# time :2015-10-20

'''
task_list={
	"id":(str),********************
	"ovs_link":(list),
	"ovs_tube_link":(list),********************
	"ovs_list":(list),
	"host_list":(list),********************
	"state":(str)
}

ovs_link=[[link2],[link3],[link4],[link5]]

ovs_tube_link=[[link2],[link3]]********************

ovs_list=[ovs_info1,ovs_info2]

ovs_info={
	'OVS_ID':(str)
	'OVS_Name':(str)
	'OVS_IP':(str)
	'OVS_HOST_IP':(str)********************
	'OVS_Start_Ip':(str)
	'OVS_End_Ip':(str)
	'OVS_Docker_Num':(int)
	'OVS_Mask':(str)
	'OVS_BroadCast':(str)
	'OVS_DNS':''(str)
	'OVS_State':(str)********************
}


host_list=[host1,host2,host3]


host_info={
	"ip":(str),
	"docker_version":(str),
	"mem":(str),
	"cpu":(str)
}
'''

import config
from DatabaseOperator import DataOperation
from DataCompile import DataCompile
from RunOrder import RunCommand
import sys
sys.path.append('var')
import server
from control import docker_operate
import traceback  
import socket 
import struct

class NetTopo:
	#init
	def __init__(self ):
		self.compile = DataCompile()
		self.runOrder = RunCommand()

	#Create new virtual switch node 
	# connect controller 
	def connectController(self ,Ovs_Switchs):
		if len(Ovs_Switchs) <= 0:
			return False
		for switch in Ovs_Switchs:
			Order = 'ovs-vsctl set-controller '+switch['OVS_ID']+' tcp:'+config.floodlight_host+':'+config.floodlight_port
			print Order
			self.runOrder.runCommand(Order)


	#Create new virtual switch node 
	def buildSwitchs(self,Ovs_Switchs):
		#compile data and excute order compiled to create new switch

		if len(Ovs_Switchs) <= 0:
			return False
		for switch in Ovs_Switchs:
			if self.judgeSwitchExists(switch['OVS_ID']):
				print 'bridge named '+switch['OVS_ID']+' is exists in net!'
				return False
		for switch1 in Ovs_Switchs:
			# print switch1['OVS_ID']
			if switch1['OVS_HOST_IP'] != config.Host_IP:
				continue
			Order = self.compile.compile_Switch(switch1)
			re = self.runOrder.runCommand(Order[0])
			if len(re) == 0:
				print 'bridge named '+switch1['OVS_ID']+' build succeed!'
		self.connectController(Ovs_Switchs)
		return True

	#find ip belong which sub Net
	def find(self,ip,ovs_info):
		int_ip = socket.ntohl(struct.unpack('i',socket.inet_aton(ip))[0])
		for ovs in ovs_info:
			start = socket.ntohl(struct.unpack('i',socket.inet_aton(ovs['OVS_Start_Ip']))[0])
			end = socket.ntohl(struct.unpack('i',socket.inet_aton(ovs['OVS_End_Ip']))[0])
			if start <= int_ip and int_ip >= end:
				return ovs
		return None

	# judge Switch link exists??
	def judge_Switch_link(self,link,Topo):
		Switch_links = Topo['link_linst']


	#add flows
	def add_Flows(self,src_ovs,dest_ovs,Topo):
		# if 
		pass


	#judge switch bridge exists or not
	def judgeSwitchExists(self ,switch_name):
		try:
			br_list = self.runOrder.compileReturnResault('ovs-vsctl list-br')
			print br_list
			for br in br_list:
				if switch_name == br:
					return True
		except:
			print str(traceback.format_exc())
		return False

 	#Build Switchs' link net

	def buildSwitch_Links(self,Ovs_Switchs_link):
		# Ovs_Switchs_link = self.switchs.getDataOvs_Link_info()
		for ovs_switch in Ovs_Switchs_link:
			Orders = self.compile.compile_Switch_Link(ovs_switch)
			for order in Orders:
				print order
				re = self.runOrder.runCommand(order)
				if len(re) > 0:
					print 'link net create failed!'
					return False
		return True

	#build link with switchs and docker node created
	def buildDocker_Link_Switch(self,Topo):
		try:
			docker = docker_operate()
			docker.resolve(Topo)
		except:
			print str(traceback.format_exc())
			return False
		return True

	#build net topo 
	def buildNet_Topo(self,Task):
		Topo = self.compile.compileMessge(Task)

		if self.buildSwitchs(Topo[0]) :
			if self.buildSwitch_Links(Topo[1]) and self.build_Net_Gre(Topo[2]):
				# if self.buildDocker_Link_Switch(Task):
				print 'Topo net create succeed!'
				return True
			else :
				print 'Topo net create failed!'
				return False

	#del all switch 
	def del_switchs(self):
		br_list = self.runOrder.compileReturnResault('ovs-vsctl list-br')
		for br in br_list:
			re = self.runOrder.runCommand('ovs-vsctl del-br '+br)
			print 'delete bridge succeed!'+br

	#del all docker node of topo
	def del_Docker_Node(self):
		#need talking makesure table struct
		docker_list1 = self.runOrder.compileReturnResault('docker ps -aq')
		if len(docker_list1) <= 0:
			return True
		docker_list2 = self.runOrder.compileReturnResault('docker kill $(docker ps -aq)')
		docker_list3 = self.runOrder.compileReturnResault('docker rm $(docker ps -aq)')
		if len(docker_list3) == len(docker_list1):
			return True
		else:
			return False

	#build Net grep 
	def build_Net_Gre(self,Ovs_tube_link):
		if len(Ovs_tube_link) <= 0:
			return True
		for tube_link in Ovs_tube_link:
			Orders = self.compile.compile_Gre_Link(tube_link)
			try:
				for order in Orders:
					re = self.runOrder.runCommand(order)
			except:
				print str(traceback.format_exc())
				return False
		return True

topo = NetTopo()
topo.find('127.0.0.1',[{'OVS_Start_Ip':'101.0.0.1','OVS_End_Ip':'102.0.0.2'}])
# topo.del_switchs()
# topo.buildNet_Topo(server.demo())
