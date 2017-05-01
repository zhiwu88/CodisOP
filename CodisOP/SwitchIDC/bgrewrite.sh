#!/bin/bash

source /etc/profile
source /home/work/.bashrc

xyHostList=`cml $1 xy | awk '{print $4}'`
yzHostList=`cml $1 yz | awk '{print $4}'`
xyHost=`cml $1 xy | head -1 | awk '{print $4}'`


for ip in $xyHostList
do
  for port in 6000 6002 6002 6003 6004 6005
  do
    echo "bgrewriteaof------>$ip--$port"
    echo "bgrewriteaof" | ./redis-cli -h $ip -p $port
    sleep 5
  done
done

echo "sleep 60"
while ((n<=60))
do
  ((++n))
  echo -ne "${n}s\r"
  sleep 1
done

for ip in $xyHostList
do 
  for port in 6000 6002 6002 6003 6004 6005
  do 
    echo "bak aof------>$ip--$port"
    ssh $ip "cd /home/work/codis_$port/data && cp appendonly.aof appendonly.aof.bak"
  done
done
