
#port
PORT_LIST=("6000" "6001" "6002" "6003" "6004" "6005" "7000" "7001" "7002" "7003" "7004" "7005")
#XY_PORT_LIST=("6000" "6001" "6002" "6003" "6004" "6005" )
#YZ_PORT_LIST=("8000" "8001" "8002" "8003" "8004" "8005" )
#YZ_PORT_LIST=("8000" "8001" "8002" "8003" "8004" "8005" "8006" "8007" "8008" "8009" "8010" "8011")

source /etc/profile
source /home/work/.bashrc

if [[ $# != 2 ]];then
  echo "Usage:"
  echo "    codismem codisName debug/verbose/notice/warning"
  echo ""
  exit
fi

xyHostList=`cml $1 xy | awk '{print $4}'`

if [[ $xyHostList == '' ]];then
  echo ""
  echo "error:can't find codisName:"$1
  echo ""
  exit
fi

echo -n "are you sure?[y/n]:"
read confirm
if [[ $confirm != 'y' ]];then 
  exit
fi  


for IP in $xyHostList
do
for PORT in ${PORT_LIST[@]}
do
    echo "=================="
    echo $IP $PORT
    echo "=================="
    logparameter=$2
    #echo "config get loglevel" | /home/work/CodisOP/BinSrc/redis-cli -h $IP -p $PORT
    echo "config set loglevel $logparameter" | /home/work/CodisOP/BinSrc/redis-cli -h $IP -p $PORT
    echo 'config rewrite'| /home/work/CodisOP/BinSrc/redis-cli -h $IP -p $PORT
    echo "config get loglevel" | /home/work/CodisOP/BinSrc/redis-cli -h $IP -p $PORT
done
done

yzHostList=`cml $1 yz | awk '{print $4}'`
for IP in $yzHostList
do
for PORT in ${PORT_LIST[@]}
do
    echo "=================="
    echo $IP $PORT
    echo "=================="
    logparameter=$2
    #echo "config get loglevel" | /home/work/CodisOP/BinSrc/redis-cli -h $IP -p $PORT
    echo "config set loglevel $logparameter" | /home/work/CodisOP/BinSrc/redis-cli -h $IP -p $PORT
    echo 'config rewrite'| /home/work/CodisOP/BinSrc/redis-cli -h $IP -p $PORT
    echo "config get loglevel" | /home/work/CodisOP/BinSrc/redis-cli -h $IP -p $PORT
done
done
