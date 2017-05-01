# -*- encoding:utf-8 -*-

import sys
import commands

def Yumrepo_xy(hostlist):
    for host in hostlist:
        rst = commands.getoutput("ssh %s 'cd /etc/yum.repos.d && mkdir /etc/yum.repos.d/bak && mv /etc/yum.repos.d/*.repo bak/ && wget http://100.0.0.2/centos_epel_full.repo && yum clean all && yum makecache' " % host )
        print rst
        print "____________已完成 YUM 源安装。[ok]"

def Yumrepo_yz(hostlist):
    for host in hostlist:
        rst = commands.getoutput("ssh %s 'cd /etc/yum.repos.d && mkdir /etc/yum.repos.d/bak && mv /etc/yum.repos.d/*.repo bak/ && wget http://100.0.0.1/centos_epel_full.repo && yum clean all && yum makecache' " % host )
        print rst
        print "____________已完成 YUM 源安装。[ok]"

def main():

    user = commands.getoutput('whoami')
    if user != 'root':
        print "user is not root"
        exit()

    hostlist = []
    with open('hostlist', 'r') as f:
        for line in f.readlines():
            hostlist.append(line.strip())

    print "_____本次将要修改 Yum repo 的服务器IP地址："  
    for host in hostlist:
            print host

    confirm1 = raw_input("***** 请核实即将操作的IP地址，无误后确认修改Yum仓库配置！！！*****\n请确认【yes/no】:")
    if confirm1 != 'yes':
            exit()

    IDC = raw_input("***** 请选择服务器所在的机房 ？？？******\n晓月请输入xy，亦庄请输入yz。【xy/yz】:")
    if IDC == 'xy':
        print "执行晓月xy YUM源安装操作 ... ..."
        Yumrepo_xy(hostlist)
    elif IDC == 'yz':
        print "执行亦庄yz YUM源安装操作 ... ..."
        Yumrepo_yz(hostlist)
    else:
        print "输入有误！"
        exit()


if __name__ == "__main__":
    main()

