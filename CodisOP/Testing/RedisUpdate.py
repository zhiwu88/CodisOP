#! /usr/bin/env python

import urllib2
import json
from pprint import pprint
import commands

def GetServerIP(IP):
    GroupAPI = 'http://' + IP + ':8080/api/server_groups'
    response = urllib2.urlopen(GroupAPI)
    page_str = response.read()
    group_json_list = json.loads(page_str)
    IPList = set()
    for group in group_json_list:
        for server in group["servers"]:
            #pprint(server["addr"].split(':')[0])
            IPList.add(server["addr"].split(':')[0])
    return IPList

def RedisUpdate(IPList,PortList):
    for IP in IPList:
        print "_______Update Redis in ",IP
        res1 = commands.getoutput("scp {0} {1}:/home/work/codis-server".format('redis-server', IP))
        res2 = commands.getoutput("ssh {0} 'md5sum codis-server'".format(IP))
        print res1,res2
        for Port in PortList:
            print "__", Port, "__"
            res3 = commands.getoutput("ssh {0} 'cd /home/work/codis_{1}/bin/ && mv codis-server codis-server_bak && cp /home/work/codis-server . && md5sum /home/work/codis_{1}/bin/codis-server'".format(IP, Port))
            print res3

def RedisConfUpate(IPList,PortList):
    for IP in IPList:
        print "_______Update Redis Configure in ",IP
        res1 = commands.getoutput("scp {0} {1}:/home/work/redis.conf".format('redis.conf', IP))
        res2 = commands.getoutput("ssh {0} 'md5sum redis.conf'".format(IP))
        print res1,res2
        for Port in PortList:
            print "__", Port, "__"
            res3 = commands.getoutput("ssh {0} 'cd /home/work/codis_{1}/conf/ && mv redis.conf redis.conf_bak && cp /home/work/redis.conf . && md5sum redis.conf && sed -i \'s/7000/{1}/g\' redis.conf '".format(IP, Port))
            print res3


def RedisBack(IPList,PortList):
    for IP in IPList:
        print "_______Back Redis in ",IP
        res1 = commands.getoutput("scp {0} {1}:/home/work/codis-server_old".format('bin/codis-server_old', IP))
        res2 = commands.getoutput("ssh {0} 'md5sum codis-server_old'".format(IP))
        print res1,res2
        for Port in PortList:
            print "__", Port, "__"
            res3 = commands.getoutput("ssh {0} 'cd /home/work/codis_{1}/bin/ && mv codis-server codis-server_bak && cp /home/work/codis-server_old codis-server && md5sum /home/work/codis_{1}/bin/codis-server'".format(IP, Port))
            print res3

def RedisConfBack(IPList,PortList):
    for IP in IPList:
        print "_______Back Redis Configure in ",IP
        res1 = commands.getoutput("scp {0} {1}:/home/work/redis.conf_old".format('bin/redis_old.conf', IP))
        res2 = commands.getoutput("ssh {0} 'md5sum redis.conf'".format(IP))
        print res1,res2
        for Port in PortList:
            print "__", Port, "__"
            res3 = commands.getoutput("ssh {0} 'cd /home/work/codis_{1}/conf/ && mv redis.conf redis.conf_bak && cp /home/work/redis.conf_old redis.conf && md5sum redis.conf && sed -i \'s/7000/{1}/g\' redis.conf '".format(IP, Port))
            print res3


def main():
    DashboardIP = '100.0.0.1'
    PortList = [6000,6001,6002,6003,6004,6005,7000,7001,7002,7003,7004,7005]
    IPList = GetServerIP(DashboardIP)
    print(IPList)
    RedisUpdate(IPList,PortList)
    RedisConfUpate(IPList,PortList)
    #RedisBack(IPList,PortList)
    #RedisConfBack(IPList,PortList)


if __name__ == "__main__":
    main()

