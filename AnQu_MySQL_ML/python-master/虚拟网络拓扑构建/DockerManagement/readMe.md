#introduce files

###ReadMe.md：程序运行环境，和运行入口介绍；
##Config.py : 是系统全局变量，主要是系统执行的一些所需外部参数配置；
##Ovs.xml : 是系统执行的一个用例，介绍数据解析源xml格式
##Virtual_docker_node_Client.py : 系统数据接收客户端，也是模拟节点的入口
##unOrder.py : 系统命令执行类
##DockerManagement.py : docker 管理类 （未实现）
##DatabaseOperrator.py : 数据库操作
##Data_server.py : 测试使用的数据发送服务器端
##DataCompile.py : json数据解析，生成构建Topo图的命令
##BuiltTopo.py ：构建拓扑图类


# run envirunment introduce

# install docker and download image from net

# install openVSwicth 2.3

# install ovs-docker 

# install pipework

# package needed for this process 

# packages : zmq pymongo simplejson 

#pre run 
# path floodlight :/home/floodlight/target
$>

#run process on root mod
$>python Virtual_docker_node_Client.py   #client receive json data struct and run to build Topo

$>pyhton Data_Server.py                  #server compile xml file and send resault to client


!!!!!this program only run create topo case!!!!!! 




