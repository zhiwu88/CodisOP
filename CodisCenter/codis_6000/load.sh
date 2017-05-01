#!/bin/sh
#
# Simple Redis init.d script conceived to work on Linux systems
# as it does use of the /proc filesystem.

Port=6000
REDIS_HOME=/home/work/CodisCenter/codis_$Port
REDIS_PORT=$Port
EXEC=$REDIS_HOME/bin/codis-server
CLIEXEC=$REDIS_HOME/bin/redis-cli

PIDFILE=$REDIS_HOME/log/redis.pid
CONF="$REDIS_HOME/conf/redis.conf"

echo never > /sys/kernel/mm/transparent_hugepage/enabled
case "$1" in
    start)
        $EXEC $CONF
        ;;
    stop)
        $CLIEXEC -p $Port shutdown
        ;;
    restart)
        stop
        start
        ;;
    *)
        echo "Please use start or stop as first argument"
        ;;
esac
