#coding=utf-8
'''
@作者：陈晨
@时间：2015.10.25
@功能：docker创建调度
'''




import copy

'''
host={
	
	"ip":"127.0.0.1",
	"docker_version":"1.7.1",
	"remain_mem":0,
	"cpu":0,
	"exist_docker":0,
	"run_docker":0
}

'''
class scheduler():
	def __init__(self):
		pass

	'''
	def cul_min(self,hosts):
		min_id=0
		min_docker=1000000
		for num in xrange(0,len(hosts)):
			if hosts[num]["exist_docker"]<min_docker:
				min_docker=hosts[num]["exist_docker"]
				min_id=num

		return min_id


	def balance(self,create_operation):
		creates=[]
		hosts_docker= copy.deepcopy(self.hosts)
		for num in xrange(0,create_operation["create_num"]):
			min_host=self.cul_min(hosts_docker)
			hosts_docker[min_host]["exist_docker"]+=1

		for host_id in xrange(0,len(hosts_docker)):
			create_num=hosts_docker[host_id]["exist_docker"]-self.hosts[host_id]["exist_docker"]
			if create_num!=0:
				create={
					"host":self.hosts[host_id]["ip"],
					"version":self.hosts[host_id]["docker_version"],
					"create_num":create_num,      #创建个数
					"name_pro":create_operation["name_pro"],     #待创建容器前缀名
					"image":create_operation["image"]    #选择镜像名称或id
				}
				creates.append(create)

		return creates

	'''
	def docker_scheduler(self,ovs_list,host_list,list_relation):
		create_list=[]
		ovs_lists=[]
		for ovs in ovs_list:
			create={
			"host":host_list[0]["ip"],
			"version":host_list[0]["docker_version"],
			"create_num":ovs["OVS_Docker_Num"],      #创建个数
			'start_ip':ovs["OVS_Start_Ip"],
			'end_ip':ovs["OVS_End_Ip"],
			'mask':ovs["OVS_Mask"],
			"name_pro":ovs["OVS_ID"],     #待创建容器前缀名
			"image":ovs["OVS_Image"],    #选择镜像名称或id
			"ovs_id":ovs["OVS_ID"],
			}
			ovs['OVS_HOST_IP']=host_list[0]["ip"]
			create_list.append(create)
			ovs_lists.append(ovs)
		operation={
		"type":"create",
		"operation":create_list
		}
		return operation,ovs_lists,[]

if __name__ == '__main__':
	import resolve_xml_ovs
	example=scheduler()
	list_ovs,list_relation=resolve_xml_ovs.get_xml_ovs()
	list_host=resolve_xml_ovs.get_xml_host_conf()
	print example.docker_scheduler(list_ovs,list_host,list_relation)

