#!/bin/bash

source /etc/profile
source /home/work/.bashrc

#危险脚本，平时注释掉productList变量
##productList=("hundred" "rank-cache" "hb" "reward" "notice" "public" "linkface" "api" "jiaoyi" "friend" "ermas" "repayment" "payui" "coupon" "feed" "hadoop" "huodong")

for product in ${productList[@]}
do
  echo "==============="
  echo      $product
  echo "==============="
  xyHostList=`cml $product xy | awk '{print $4}'`
  for xyIP in ${xyHostList}
  do
    echo "stop ha"
    ssh $xyIP 'source /etc/profile && cd /home/work/ha && sh load.sh stop'
    sleep 1
    echo "stop dashboard"
    ssh $xyIP 'source /etc/profile && cd /home/work/dashboard && sh load.sh stop'
    sleep 1
    echo "stop proxy_9100"
    ssh $xyIP 'source /etc/profile && cd /home/work/proxy_9100 && sh load.sh stop'
    sleep 1
    echo "stop proxy_9200"
    ssh $xyIP 'source /etc/profile && cd /home/work/proxy_9200 && sh load.sh stop'
    sleep 1
  done

  for xyIP in ${xyHostList}
  do
    if [[ $xyIP =~ "10.0.0." ]]
    then 
      echo $xyIP
      echo "stop codis_6000"
      ssh $xyIP 'source /etc/profile && cd /home/work/codis_6000 && sh load.sh stop'
      sleep 1
      echo "stop codis_6001"
      ssh $xyIP 'source /etc/profile && cd /home/work/codis_6001 && sh load.sh stop'
      sleep 1
      echo "stop codis_6002"
      ssh $xyIP 'source /etc/profile && cd /home/work/codis_6002 && sh load.sh stop'
      sleep 1
      echo "stop codis_6003"
      ssh $xyIP 'source /etc/profile && cd /home/work/codis_6003 && sh load.sh stop'
      sleep 1
      echo "stop codis_6004"
      ssh $xyIP 'source /etc/profile && cd /home/work/codis_6004 && sh load.sh stop'
      sleep 1
      echo "stop codis_6005"
      ssh $xyIP 'source /etc/profile && cd /home/work/codis_6005 && sh load.sh stop'
      sleep 1
      echo "stop codis_7000"
      ssh $xyIP 'source /etc/profile && cd /home/work/codis_7000 && sh load.sh stop'
      sleep 1
      echo "stop codis_7001"
      ssh $xyIP 'source /etc/profile && cd /home/work/codis_7001 && sh load.sh stop'
      sleep 1
      echo "stop codis_7002"
      ssh $xyIP 'source /etc/profile && cd /home/work/codis_7002 && sh load.sh stop'
      sleep 1
      echo "stop codis_7003"
      ssh $xyIP 'source /etc/profile && cd /home/work/codis_7003 && sh load.sh stop'
      sleep 1
      echo "stop codis_7004"
      ssh $xyIP 'source /etc/profile && cd /home/work/codis_7004 && sh load.sh stop'
      sleep 1
      echo "stop codis_7005"
      ssh $xyIP 'source /etc/profile && cd /home/work/codis_7005 && sh load.sh stop'
      sleep 1
    fi
  done 

  echo "==================="
  echo      $product "done"
  echo "==================="
done

#echo "stop zk"
#ssh 10.0.0.2 'source /etc/profile && cd /home/work/zookeeper && sh load.sh stop'
#sleep 5
#ssh 10.0.0.3 'source /etc/profile && cd /home/work/zookeeper && sh load.sh stop'
#sleep 5
#ssh 10.0.0.4 'source /etc/profile && cd /home/work/zookeeper && sh load.sh stop'
