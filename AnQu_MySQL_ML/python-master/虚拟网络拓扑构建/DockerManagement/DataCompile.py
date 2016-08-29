#-*- utf-8 -*-
# writer : lgy
# time :2015-10-19

import simplejson
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

ovs-vsctl add-br tech-br
ovs-vsctl add-port tech-br tep0 -- set interface tep0 type=internal
ifconfig tep0 192.168.1.1 netmask 255.255.255.0
ovs-vsctl add-br sdn-br0
ovs-vsctl set bridge sdn-br0 stp_enable=true
ovs-vsctl add-port sdn-br0 gre0 -- set interface gre0 type=gre options:remote_ip=192.168.5.31
brctl addbr br0
ip link set dev br0 up
brctl addbr br1
ip link set dev br1 up

ovs-vsctl add-br ovs0
ovs-vsctl set bridge ovs0 stp_enable=true
ovs-vsctl add-port ovs0 br0
ovs-vsctl add-port ovs0 br1
'''
class DataCompile:
	def __init__(self):
		pass
	#OVS_IP table analysis for switchs build order
	def compile_Switch(self,OVS_Ip):
		Ovs_Order = []
		print OVS_Ip
		# if OVS_Ip['OVS_HOST_IP'] == config.Host_IP
		print OVS_Ip['OVS_ID']
		Switch = OVS_Ip['OVS_ID']
		Ovs_Order.append('ovs-vsctl add-br '+Switch)
		return Ovs_Order

	#OVS_link table analysis for switchs' link  build order
	def compile_Switch_Link(self , swicth_link):
		Link_Order = []
		#build switch link order
		S = swicth_link[0]
		T = swicth_link[1]
		StoT = S+'_to_'+T
		TtoS = T+'_to_'+S
		Link_Order.append('ovs-vsctl add-port '+S+' '+StoT)
		Link_Order.append('ovs-vsctl set interface '+StoT+' type=patch')
		Link_Order.append('ovs-vsctl set interface '+StoT+' options:peer='+TtoS)
		Link_Order.append('ovs-vsctl add-port '+T+' '+TtoS)
		Link_Order.append('ovs-vsctl set interface '+TtoS+' type=patch')
		Link_Order.append('ovs-vsctl set interface '+TtoS+' options:peer='+StoT)
		return Link_Order

	# docker link switch 
	def compile_Docker_Link_Switch(self , docker_links):
		Docker_Link = []

	#gre link with other host
	def compile_Gre_Link(self,ovs_tube_link):
		Orders = []
		bridge1 = ovs_tube_link[0]['OVS_ID']
		bridge2 = ovs_tube_link[1]['OVS_ID']
		link_host = ovs_tube_link[1]['OVS_HOST_IP']
		local_gre = bridge1+'_GreTo_'+bridge2
		link_gre = bridge2+'_GreTo_'+bridge1
		Orders.append('ovs-vsctl set bridge '+bridge+' stp_enable=true')
		Orders.append('ovs-vsctl add-port '+ovs_tube_link[0]+' '+local_gre+' -- set interface '+link_gre+\
					' type=gre options:remote_ip='+link_host)
		return Orders
	
	#message translation
	def compileMessge(self,task):
		Topo = []
		Topo.append(task['ovs_list'])
		Topo.append(task['ovs_link'])
		Topo.append(task['ovs_tube_link'])
		return Topo








