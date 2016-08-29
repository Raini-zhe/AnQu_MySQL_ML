$!/usr/bash
## _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-27
# start hadoop , hive , spark

source /etc/profile

# sudo s
#start hadoop
hivefilePath=/home/mysql1/anqu/python/RecieveFileData 
filePath=/home/mysql1
cd $filePath/hadoop/
./sbin/start-dfs.sh
# ./sbin/start-yarn.sh

#start hive 
cd $hivefilePath
#source /etc/profile
hive --service metastore &
hive --service hiveserver2 &

#start spark 
cd $filePath/spark
./sbin/start-all.sh

export PATH=$PATH:/home/mysql1/spark/python
source /etc/profile

# show 
jps 
source /etc/profile
subl

