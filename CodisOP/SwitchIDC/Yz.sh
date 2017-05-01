#!/bin/bash
source ~/.bashrc

xyHostList=`cml $1 xy | awk '{print $4}'`
yzHostList=`cml $1 yz | awk '{print $4}'`
xyHost=`cml $1 xy | head -1 | awk '{print $4}'`

python qiejifang.py $1 $xyHost

scp tmp/${1}*.sh $xyHost:/home/work/dashboard/

ssh $xyHost "source /etc/profile && cd /home/work/dashboard/ && sh ${1}-proYz.sh"

for yzip in $yzHostList
do
  echo "restart Yz proxy"
  echo $yzip
  ssh $yzip 'source /etc/profile && cd /home/work/proxy_9100 && sh load.sh stop && sleep 1 && sh load.sh start'
  ssh $yzip 'source /etc/profile && cd /home/work/proxy_9200 && sh load.sh stop && sleep 1 && sh load.sh start'
done
