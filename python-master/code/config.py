#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-13
#，软件系统全局变量 ------ 变量声明

#

Host_IP = '127.0.0.1'    #config to you database host address
database_en = 'mysql_anqu_en'  # english  
database_chi = 'mysql_anqu_chi' #chinese
database_japan = 'mysql_anqu_japan' #japanese
# add your database depend on your need
# database_XXX  
dataBase = database_chi
dataBase_port = 3306    #config to your database port 
dataBase_user = 'root'  #config to your database user
dataBase_passwd = 'root'#config to your database user's password

#xiang guan de biao 
# hintWord = 'hintword'   
hintWord = 'searchHint'


#系统运行各模块包路径

fileResaultPath = '/home/mysql1/anqu/analysisResault/'  #config the path what you want
fileClassResaultPath = fileResaultPath + 'ClassWord'
fileKeyWordResaultPath = fileResaultPath + 'KeyWord'
fileObjectPath = fileResaultPath + "Object"
fileRootPath = '/home/mysql1/anqu/python/code/'        #config the path being the point your code was contained ! 
fileToolsPath = fileRootPath + "Tools"
fileWordsPath = fileRootPath+'Word'
fileAnalysisPath = fileRootPath+'analysis'
fileDataPath = fileRootPath + 'data_deal'
fileClusterPath = fileRootPath + 'Cluster'
fileWordAnalysisPath = fileRootPath + 'wordAnalysis'

#系统运行，以来包路径配置
import sys
sys.path.append(fileRootPath)
sys.path.append(fileDataPath)
sys.path.append(fileAnalysisPath)
sys.path.append(fileWordsPath)
sys.path.append(fileWordAnalysisPath)
sys.path.append(fileToolsPath)
sys.path.append(fileClusterPath)
reload(sys)
sys.setdefaultencoding('utf8') 

