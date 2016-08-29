$!/usr/bash
## _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-27
# stop hadoop , hive , spark

# sudo s

filePath=/home/mysql1/ 

#stop spark 
cd $filePath/spark
./sbin/start-all.sh

#stop hadoop
cd $filePath/hadoop/
./sbin/start-dfs.sh




