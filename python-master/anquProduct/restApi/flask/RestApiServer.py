#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-08-05
import sys
sys.path.append('/home/mysql1/anqu/python/anquProduct/Server')
reload(sys)
sys.setdefaultencoding('utf8')
import config

from HqlSpark import HqlSpark as HS
#!flask/bin/python
from flask import Flask, jsonify
from flask import request
from flask import abort
import json


app = Flask(__name__)
mysql = HS()

def runAnalysis(pare=None):
    task_j = json.dumps(pare)
    ta = json.loads(task_j)
    re = ta.keys()[0]
    pa_dic = json.loads(re)
    lan = pa_dic['language']
    return {"answer":pa_dic}
    # return jsonify({'answer':pare})

def A(num1,num2):
	print "My first Rest API"
	return num1+num2

@app.route('/test', methods=['POST'])
def call_analysis():
    if request.json:
        abort(400)
    data = request.form
    return jsonify({'task': runAnalysis(data)}), 201

if __name__ == '__main__':
    app.run(debug=True)