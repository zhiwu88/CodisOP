# -*- encoding:utf-8 -*-

import sys
import commands


yz_zk_list = ['100.0.0.4','100.0.0.5','100.0.0.6']


def modify_cfg(hostlist):
    for host in hostlist:
        print "modify" , host
        rst = commands.getoutput("ssh %s 'sed -i \"/peerType/ s/^/&#/;/10.0/ s/^/&#/;s/:observer//g\" /home/work/zookeeper/conf/zoo.cfg && cat /home/work/zookeeper/conf/zoo.cfg|grep -v \"#\|^$\" '" % host)
        print rst
        print "_________________________"

def zk_data(hostlist):
    for host in hostlist:
        print "backup data in" , host
        rst = commands.getoutput("ssh %s 'mv /home/work/zookeeper/data/version-2 /home/work/zookeeper/data/version-2_`date +%%Y%%m%%d` && cp -r /home/work/zookeeper/data/zk_data_rsync/ /home/work/zookeeper/data/version-2/ '" % host)
        print rst
        print "_________________________"

def restart_zk(hostlist):
    for host in hostlist:
        print "Restart zookeeper in" , host
        rst = commands.getoutput("ssh %s 'sh /home/work/zookeeper/load.sh start'" % host)
        print rst


def main():

    confirm1 = raw_input("***** 警告：本操作只适用在晓月苑机房发生灾难性事故处理！！！*****\n请确认【yes/no】:")
    if confirm1 != 'yes':
        exit()

    print "_____亦庄ZooKeeper地址："  
    for yzzk in yz_zk_list:
            print yzzk

    confirm2 = raw_input("***** 请核实亦庄ZooKeeper地址，无误后确认修改亦庄ZK zoo.cfg 配置！！！*****\n请确认【yes/no】:")
    if confirm2 != 'yes':
            exit()

    modify_cfg(yz_zk_list)
    print "_____已完成修改亦庄ZooKeeper zoo.cfg 配置。\n\n"

    confirm3 = raw_input("***** 即将把亦庄ZK的数据备份，使用从晓月同步过来的事务日志和快照！*****\n请确认【yes/no】:")
    if confirm3 != 'yes':
            exit()

    zk_data(yz_zk_list)
    print "_____已完成rsync备份的数据替换已有的可能过期的快照。\n\n"

    confirm4 = raw_input("***** 现在重启亦庄 ZooKeeper ！！！******\n请确认【yes/no】:")
    if confirm4 != 'yes':
            exit()

    restart_zk(yz_zk_list)
    print "_____已完成Zookeeper进程重启。"
    print "_____为确保Codis集群工作正常，请重启Codis集群Proxy ！！！。"


if __name__ == "__main__":
    main()

