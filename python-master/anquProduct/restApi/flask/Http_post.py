#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-08-06


#!flask/bin/python
import urllib
import urllib2
import json
# from flask import Flask,jsonify
    
def http_post():
	url='http://127.0.0.1:5000/test'
	# values ={'user':'Smith','passwd':'123456'}
	pare = {
				# 'task':{
					'language':'cn',
					'appIds':[
						{"appid":'123456789'},
		    			{"appid":'123456789'}],
		    		'ClusterNum':20,
		    		'WordNum':50,
		    		'ShowOnWebPage':True,
		    		'EmailMessage':True
    			# }
    		}
    # print pare
	jdata = json.dumps(pare)				# 对数据进行JSON格式化编码
	# print jdata
	req = urllib2.Request(url, jdata)       # 生成页面请求的完整数据
	response = urllib2.urlopen(req)       # 发送页面请求
	return response.read()                    # 获取服务器返回的页面信息

resp = http_post()
print resp