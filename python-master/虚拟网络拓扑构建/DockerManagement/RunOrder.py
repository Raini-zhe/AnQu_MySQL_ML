#-*- utf-8 -*-
# writer : lgy
# time: 2015-10-18
import os

class RunCommand:
	def __init__(self):
		pass
	#excute order 
	def runCommand(self,Order):
		tmp = os.popen(Order).readlines()
		return tmp

	#compile return resualt after run order
	def compileReturnResault(self,Order):
		resaults = self.runCommand(Order)
		# print resaults
		new_resualt = []
		for resault in resaults:
			new_resualt.append(resault.strip('\n'))
		return new_resualt



# ex = RunCommand()
# # print ex.runCommand('sudo -P --prompt=liguoyu su')
# print ex.compileReturnResault('ovs-vsctl list-br')
# # print 'succeed'
