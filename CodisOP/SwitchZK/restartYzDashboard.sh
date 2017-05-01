#!/bin/bash

source /etc/profile
source /home/work/.bashrc

xyHostList=`cml $1 xy | awk '{print $4}'`
yzHostList=`cml $1 yz | awk '{print $4}'`

#for xyip in $xyHostList
#do
#  echo $xyip
#  ssh $xyip 'source /etc/profile && cd /home/work/dashboard && sh load.sh stop && sleep 1 && sh load.sh start'
#  ssh $xyip 'source /etc/profile && cd /home/work/dashboard && sh load.sh stop && sleep 1 && sh load.sh start'
#done 

for yzip in $yzHostList
do
  echo $yzip
  ssh $yzip 'source /etc/profile && cd /home/work/dashboard && sh load.sh stop && sleep 1 && sh load.sh start'
  ssh $yzip 'source /etc/profile && cd /home/work/dashboard && sh load.sh stop && sleep 1 && sh load.sh start'
done
