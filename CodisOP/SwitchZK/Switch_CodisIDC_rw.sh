#!/bin/bash
source ~/.bashrc

#
# sh Switch_CodisIDC_rw.sh CodisName
#

yzHostList=`cml $1 yz | awk '{print $4}'`
yzHost=`cml $1 yz | head -1 | awk '{print $4}'`

python Switch_CodisIDC_01_create.py $1 $yzHost

scp tmp/${1}*.sh $yzHost:/home/work/dashboard/
ssh $yzHost "source /etc/profile && cd /home/work/dashboard/ && sh ${1}-proYz.sh"

#for yzip in $yzHostList
#do
#  echo "restart Yz proxy"
#  echo $yzip
#  ssh $yzip 'source /etc/profile && cd /home/work/proxy_9100 && sh load.sh stop && sleep 1 && sh load.sh start'
#  ssh $yzip 'source /etc/profile && cd /home/work/proxy_9200 && sh load.sh stop && sleep 1 && sh load.sh start'
#done
