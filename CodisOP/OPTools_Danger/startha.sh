#!/bin/bash

source /etc/profile
source /home/work/.bashrc

#危险脚本，平时注释掉productList变量。
#productList=("hundred" "hb" "reward" "notice" "public" "linkface" "api" "jiaoyi" "friend" "ermas" "repayment" "payui" "coupon" "feed" "hadoop" "huodong")

for product in ${productList[@]}
do
  echo "==============="
  echo      $product
  echo "==============="
  xyHostList=`cml $product xy | awk '{print $4}'`


  for xyIP in ${xyHostList}
  do
    echo "start ha" $xyIP
    ssh $xyIP 'source /etc/profile && cd /home/work/ha && sh load.sh start'
    sleep 1
  done

  echo "==================="
  echo      $product "done"
  echo "==================="
done

#echo "start zk"
#ssh 10.0.0.2 'source /etc/profile && cd /home/work/zookeeper && sh load.sh start'
#sleep 10
#ssh 10.0.0.3 'source /etc/profile && cd /home/work/zookeeper && sh load.sh start'
#sleep 10
#ssh 10.0.0.4 'source /etc/profile && cd /home/work/zookeeper && sh load.sh start'
