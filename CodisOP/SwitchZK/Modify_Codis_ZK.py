# -*- encoding:utf-8 -*-

import sys
import commands


#hostlist = ['10.0.0.6','10.0.0.7']
zklist_yz = "100.0.0.4:2181,100.0.0.5:2181,100.0.0.6:2181"
#zklist_xy = "10.0.0.5:2181,10.0.0.6:2181,10.0.0.7:2181"

def modify_dashboard(hostlist, zklist):
    for host in hostlist:
        print "Modify Dashboard ZK config in" , host
        rst = commands.getoutput("ssh %s 'sed -i \"/zk=/ s/^/&#/;/^#zk/a zk=%s\" /home/work/dashboard/conf/config.ini && cat /home/work/dashboard/conf/config.ini|grep -v \"#\|^$\"'" %(host,zklist))
        print rst
        print "_________________________"

def modify_proxy(hostlist, zklist):
    for host in hostlist:
        print "Modify Proxy ZK config in" , host
        rst1 = commands.getoutput("ssh %s 'sed -i \"/zk=/ s/^/&#/;/^#zk/a zk=%s\" /home/work/proxy_9100/conf/config.ini && cat /home/work/proxy_9100/conf/config.ini|grep -v \"#\|^$\"'" %(host,zklist))
        print rst1
        print "_________________________"
        rst2 = commands.getoutput("ssh %s 'sed -i \"/zk=/ s/^/&#/;/^#zk/a zk=%s\" /home/work/proxy_9200/conf/config.ini && cat /home/work/proxy_9200/conf/config.ini|grep -v \"#\|^$\"'" %(host,zklist))
        print rst2
        print "_________________________"

def restart_das_proxy(hostlist):
    for host in hostlist:
        print "Restart Dashboard and Proxy in" , host
        rst0 = commands.getoutput("ssh %s 'sh /home/work/dashboard/load.sh start'" % host)
        print rst0
        rst1 = commands.getoutput("ssh %s 'sh /home/work/proxy_9100/load.sh start'" % host)
        print rst1
        rst2 = commands.getoutput("ssh %s 'sh /home/work/proxy_9200/load.sh start'" % host)
        print rst2


def main():

    confirm1 = raw_input("***** 警告：本操作只适用在晓月苑ZooKeeper发生故障需紧急改用亦庄Zookeeper的场景！！！*****\n请确认【yes/no】:")
    if confirm1 != 'yes':
        exit()

    hostlist = []
    with open('hostlist', 'r') as f:
        for line in f.readlines():
            hostlist.append(line.strip())

    print "_____本次将要修改的Codis Cluster 地址："  
    for host in hostlist:
            print host

    confirm2 = raw_input("***** 请核实Codis Cluster地址，无误后确认修改Dashboard 和Proxy 配置！！！*****\n请确认【yes/no】:")
    if confirm2 != 'yes':
            exit()

    modify_dashboard(hostlist, zklist_yz)
    print "____________已完成修改 Dashboard 配置。[ok]\n\n"
    modify_proxy(hostlist, zklist_yz)
    print "____________已完成修改 Proxy 配置。[ok]\n\n"

    confirm3 = raw_input("***** 现在重启 Proxy ！！！******\n请确认【yes/no】:")
    if confirm3 != 'yes':
            exit()

    restart_das_proxy(hostlist)
    print "____________已完成 Dashboard, Proxy 进程重启。[ok]"


if __name__ == "__main__":
    main()

