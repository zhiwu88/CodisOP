# -*- encoding:utf-8 -*-

import sys
import commands


def ck_ss(hostlist):
    for host in hostlist:
        rst = commands.getoutput("ssh %s 'env x=\"() { :;}; echo vulnerable\" bash -c \"echo hello\"' " % host )
        print rst
        if 'vulnerable' in rst:
            print "服务器___%s___存在Bash shellshock(破壳漏洞)，请修复！" % host
        else:
            print "服务器___%s___无Bash shellshock(破壳漏洞)或者已修复。" % host

def ck_hb(hostlist):
    for host in hostlist:
        rst = commands.getoutput("ssh %s 'rpm -q -changelog openssl-1.0.1e |grep CVE-2014-0160' " % host )
        print rst
        if 'CVE-2014-0160' in rst:
            print "服务器___%s___无Openssl Heartbleed(心脏出血漏洞)或者已修复。" % host
        else:
            print "服务器___%s___存在Openssl Heartbleed(心脏出血漏洞)，请修复！" % host

def ck_glibc(hostlist):
    for host in hostlist:
        rst1 = commands.getoutput("scp ghost %s:/tmp/  " % host )
        print rst1
        rst2 = commands.getoutput("ssh %s '/tmp/ghost' " % host )
        print rst2
        if 'not vulnerable' in rst2:
            print "服务器___%s___无Glibc Ghost(幽灵漏洞)或者已修复。" % host
        else:
            print "服务器___%s___存在Glibc Ghost(幽灵漏洞)，请修复！" % host


def repair_ss(hostlist):
    for host in hostlist:
        rst = commands.getoutput("ssh %s 'yum update -y bash' " % host )
        print rst

    ck_ss(hostlist)

def repair_hb(hostlist):
    for host in hostlist:
        rst = commands.getoutput("ssh %s 'yum update -y openssl-devel openssl' " % host )
        print rst

    ck_hb(hostlist)

def repair_glibc(hostlist):
    for host in hostlist:
        rst = commands.getoutput("ssh %s 'yum update -y glibc' " % host )
        print rst

    ck_glibc(hostlist)


def main():

    user = commands.getoutput('whoami')
    if user != 'root':
        print "user is not root"
        exit()

    hostlist = []
    with open('hostlist', 'r') as f:
        for line in f.readlines():
            hostlist.append(line.strip())

    print "_____本次即将操作的服务器IP地址："  
    for host in hostlist:
            print host

    confirm1 = raw_input("***** 请核实即将操作的IP地址，确认无误后可进行漏洞检查以及漏洞修复！！！*****\n请确认【yes/no】:")
    if confirm1 != 'yes':
            exit()

    vulner = raw_input("***** 请选择漏洞 ？？？******\n-- Bash shellshock(破壳漏洞)选择'ss'，\n-- Openssl Heartbleed(心脏出血漏洞)选择'hb'，\n-- Glibc Ghost(幽灵漏洞)选'gg'。\n请选择【ss/hb/gg】:")
    what2do = raw_input("***** 请选择操作 ？？？******\n检查漏洞请输入ck，修复请输入r。【ck/r】:")
    
    if vulner == 'ss' and what2do == 'ck':
        print "执行检查Bash shellshock(破壳漏洞)操作 ... ..."
        ck_ss(hostlist)
    elif vulner == 'ss' and what2do == 'r':
        print "执行修复Bash shellshock(破壳漏洞)操作 ... ..."
        repair_ss(hostlist)
    elif vulner == 'hb' and what2do == 'ck':
        print "执行检查Openssl(心脏出血漏洞)操作 ... ..."
        ck_hb(hostlist)
    elif vulner == 'hb' and what2do == 'r':
        print "执行修复Openssl(心脏出血漏洞)操作 ... ..."
        repair_hb(hostlist)
    elif vulner == 'gg' and what2do == 'ck':
        print "执行检查glibc ghost(幽灵漏洞)操作 ... ..."
        ck_glibc(hostlist)
    elif vulner == 'gg' and what2do == 'r':
        print "执行修复glibc ghost(幽灵漏洞)操作 ... ..."
        confirm2 = raw_input("修复__glibc ghost(幽灵漏洞)__需要立即手动重启服务器，如果机器暂时不可以重启请勿继续操作，是否继续？【yes/no】")
        if confirm2 == "yes":
            repair_glibc(hostlist)
        else:
            exit()
    else:
        print "输入有误！！！"
        exit()



if __name__ == "__main__":
    main()

