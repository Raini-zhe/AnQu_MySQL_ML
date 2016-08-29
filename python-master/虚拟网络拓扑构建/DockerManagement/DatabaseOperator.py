#-*- utf-8 -*-
# writer : lgy
# time :2015-10-19

import sys
sys.path.append('/home/ovsdoc/Documents/DockerManagement')   #system path 
import config
from pymongo import MongoClient
import traceback

class DataOperation:
	def __init__(self):
		pass

	#connect mongodb database
	def connectMongo(self,host,port):
		try:
			self.client = MongoClient(host,port)
		except:
			print str(traceback.format_exc())

	#get OVS_info table's dta
	def getDataOvs_info(self):
		OVS_IP = []
		try:
			db = self.client.ovs
			table = db.ovs_info
			for data in table.find():
				OVS_IP.append(data)
		except:
			print str(traceback.format_exc())
		return OVS_IP

	#get Ovs switch node link relationship
	def getDataOvs_Link_info(self):
		OVS_LINK = []
		try:
			db = self.client.ovs
			table = db.ovs_link
			
			for link in table.find():
				OVS_LINK.append(link)
		except:
			print str(traceback.format_exc())
		return OVS_LINK

	# Insert Operation record to Operator_Log_data table
	def InsertOperator_Log_data(self,Opr_log):
		
		try:
			db = self.client.ovs
			table = db.Operator_Log_Info
			if len(Opr_log) > 0:
				table.insert(Opr_log)
		except:
			print str(traceback.format_exc())
			return -1
		return 0

	# Insert device status record into Stats_log_Info table
	def InsertStats_log_data(self,stat_log):
		try:
			db = self.client.ovs
			table = db.Stats_Log_Info
			if len(stat_log) > 0:
				table.insert(stat_log)
		except:
			print str(traceback.format_exc())
			return -1
		return 0

# op = DataOperation()
# print config.MongoDB_Host,config.MongoDB_Port
# op.connectMongo(config.MongoDB_Host,config.MongoDB_Port)
# print op.getDataOvs_Link_info()
