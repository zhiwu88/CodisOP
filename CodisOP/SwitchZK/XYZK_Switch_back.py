# -*- encoding:utf-8 -*-

import sys
import commands
import time

xy_zk_list = ['10.0.0.5','10.0.0.6','10.0.0.7']
yz_zk_list = ['100.0.0.4','100.0.0.5','100.0.0.6']


def modify_cfg_addobserver(hostlist):
    for host in hostlist:
        print "modify" , host
        rst = commands.getoutput("ssh %s 'sed -i \"/10.0/ s/$/&:observer/;/100/ s/:observer//;/zookeeper cluster/a peerType=observer\" /home/work/zookeeper/conf/zoo.cfg && cat /home/work/zookeeper/conf/zoo.cfg|grep -v \"#\|^$\" '" % host)
        print rst
        print "_________________________"

def modify_cfg_addxyobserver(hostlist):
    for host in hostlist:
        print "modify" , host
        rst = commands.getoutput("ssh %s 'sed -i \"/10.0/ s/#//;/10.0/ s/$/&:observer/\" /home/work/zookeeper/conf/zoo.cfg && cat /home/work/zookeeper/conf/zoo.cfg|grep -v \"#\|^$\" '" % host)
        print rst
        print "_________________________"

def modify_cfg_delobserver(hostlist):
    for host in hostlist:
        print "modify" , host
        rst = commands.getoutput("ssh %s 'sed -i \"/100/ s/$/&:observer/;/10.0/ s/:observer//;/peerType/d\" /home/work/zookeeper/conf/zoo.cfg && cat /home/work/zookeeper/conf/zoo.cfg|grep -v \"#\|^$\" '" % host)
        print rst
        print "_________________________"

def modify_cfg_back(hostlist):
    for host in hostlist:
        print "modify" , host
        rst = commands.getoutput("ssh %s 'sed -i \"/peerType/ s/#//;/10.0/ s/:observer//;/100/ s/$/&:observer/g\" /home/work/zookeeper/conf/zoo.cfg && cat /home/work/zookeeper/conf/zoo.cfg|grep -v \"#\|^$\" '" % host)
        print rst
        print "_________________________"

def restart_zk(hostlist):
    for host in hostlist:
        print "Restart zookeeper in" , host
        rst = commands.getoutput("ssh %s 'sh /home/work/zookeeper/load.sh start'" % host)
        print rst
        print "____________"

def stop_zk(hostlist):
    for host in hostlist:
        print "Stop zookeeper in" , host
        rst = commands.getoutput("ssh %s 'sh /home/work/zookeeper/load.sh start'" % host)
        print rst
        print "____________"

def zkdata_bak(hostlist):
    for host in hostlist:
        print "Backup zookeeper data in" , host
        rst = commands.getoutput("ssh %s 'mv /home/work/zookeeper/data/version-2 /home/work/zookeeper/data/version-2_`date +%%Y%%m%%d` '" % host)
        print rst
        print "____________"


def main():

    confirm1 = raw_input("***** 警告：本脚本仅用于测试操作流程可行性！！！ \n本操作测试在晓月苑Zookeeper已经切换至亦庄之后，晓月ZK正常后，由亦庄ZK回切到晓月ZK ！！！*****\n请确认【yes/no】:")
    if confirm1 != 'yes':
        exit()

    print "_____亦庄ZooKeeper地址："  
    for yzzk in yz_zk_list:
            print yzzk
    print "_____晓月苑ZooKeeper地址："
    for xyzk in xy_zk_list:
            print xyzk

    confirm2 = raw_input("***** 请核实亦庄和晓月ZooKeeper地址是否正确？？？\n请确认修改晓月和亦庄ZK zoo.cfg 配置，晓月ZK作为OBSERVER加入到ZK集群，备份原晓月Zookeeper数据 ！！！*****\n请确认【yes/no】:")
    if confirm2 != 'yes':
            exit()

    modify_cfg_addobserver(xy_zk_list)
    zkdata_bak(xy_zk_list)
    modify_cfg_addxyobserver(yz_zk_list)
    print "_____已完成修改亦庄和晓月ZooKeeper zoo.cfg 配置，晓月ZK节点改成observer。[OK]\n\n"
    
    confirm3 = raw_input("***** 现在重启亦庄和晓月ZooKeeper ！！！******\n请确认【yes/no】:")
    if confirm3 != 'yes':
            exit()
    
    restart_zk(yz_zk_list)
    restart_zk(xy_zk_list)
    print "_____已完成亦庄和晓月Zookeeper进程重启。[OK]"
    print "_____等待5分钟，让晓月Zookeeper与亦庄Zookeeper数据同步完成 ... ... "
    time.sleep(60)

    confirm4 = raw_input("***** 请确认晓月与亦庄ZK数据已同步完成 ！\n请确认修改亦庄ZK zoo.cfg 配置，恢复observer配置 ！*****\n请确认【yes/no】:")
    if confirm4 != 'yes':
            exit()

    modify_cfg_back(yz_zk_list)
    print "_____已完成修改亦庄ZooKeeper zoo.cfg 配置，恢复observer配置。[OK]\n\n"

    confirm5 = raw_input("***** 现在关停 亦庄ZooKeeper，以及备份原Zookeeper数据 ！！！******\n请确认【yes/no】:")
    if confirm5 != 'yes':
            exit()

    stop_zk(yz_zk_list)
    zkdata_bak(yz_zk_list)
    print "_____已完成 亦庄Zookeeper进程kill操作以及Zookeeper数据备份操作。[OK]"

    confirm6 = raw_input("***** 请确认修改晓月ZK zoo.cfg 配置，删除observer相关配置 ！！！*****\n请确认【yes/no】:")
    if confirm6 != 'yes':
            exit()
    modify_cfg_delobserver(xy_zk_list)
    print "_____已完成修改晓月ZooKeeper zoo.cfg 配置，从observer改成参与者。[OK]\n\n"

    confirm7 = raw_input("***** 现在重启 晓月ZooKeeper，以及启动亦庄ZooKeeper ！！！******\n请确认【yes/no】:")
    if confirm7 != 'yes':
            exit()

    restart_zk(xy_zk_list)
    print "_____已完成 晓月Zookeeper进程重启。[OK]"
    print "_____5分钟后启动亦庄ZooKeeper ... ..."
    time.sleep(60)
    restart_zk(yz_zk_list)


if __name__ == "__main__":
    main()

