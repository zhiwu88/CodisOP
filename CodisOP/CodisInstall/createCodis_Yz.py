#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import commands
import time
import sys
import sqlite3

def Usage():
  print ''' 
Usage:
    createCodis codisName  yzIP1,yzIP2
'''

def checkIP(ip):
  q = ip.split('.')
  return len(q) == 4 and len(filter(lambda x: x >= 0 and x <= 255,map(int, filter(lambda x: x.isdigit(), q)))) == 4

def checkExists(codisName, yzHostList):
  conn = sqlite3.connect('/home/work/CodisInstaller/tools/ClusterManager/ClusterManager.db')
  cursor = conn.execute('select * from hostinfo where hostname like "%' + codisName + '%"')
  exists = False
  for row in cursor:
    exists = True
    break
  if exists:
    print "codisName:" + codisName + " has exists!"
    conn.close()
    exit()

  for yzHost in yzHostList:
    cursor = conn.execute('select * from hostinfo where ip="' + yzHost + '"')
    exists = False
    for row in cursor:
      exists = True
      break
    if exists:
      print "IP:" + yzHost + " has exists!"
      conn.close()
      exit()

  conn.close()  

def check(codisName, yzHostList):
  if len(yzHostList) < 2 or len(yzHostList)%2 != 0:
    print "error: yzHostList%2 != 0"
    exit()

  for yzHost in yzHostList:
    ret = checkIP(yzHost)
    if not ret:
      print "IP:" + yzHost + " is not IP address!"
      exit()
    if not yzHost.startswith("100."):
      print "IP:" + yzHost + " is not yzIP"
      exit()

  cdscodisName = "cds-" + codisName
  checkExists(cdscodisName, yzHostList)

  user = commands.getoutput('whoami')
  if user != 'root':
    print "user is not root"
    exit()

def DBInsert(ip, hostName):
  insertSQL = 'insert into hostinfo(hostname, ip, used) values("%s", "%s", %d)'
  conn = sqlite3.connect('/home/work/CodisInstaller/tools/ClusterManager/ClusterManager.db')
  conn.execute(insertSQL%(hostName, ip, 1))
  conn.commit()
  conn.close()

def changeHostName(ip, hostName):
  DBInsert(ip, hostName)
  ret = commands.getoutput('ssh -n -q %s " hostname %s.jiedaibao.com && sed -i \"s/HOSTNAME=.*/HOSTNAME=%s.jiedaibao.com/\" /etc/sysconfig/network && hostname | sed \"s/\.jiedaibao.com//\" && echo \"%s.jiedaibao.com\">/proc/sys/kernel/hostname"' % (ip, hostName, hostName, hostName))
  print ret

def chown(hostList):
  for host in hostList:
    ret = commands.getoutput("ssh root@%s 'chown -R work:work /home/work'" % host)
    print ret
    ret = commands.getoutput("ssh root@%s 'chown -R work:work /var/spool/cron/work'" % host)
    print ret
    ret = commands.getoutput("ssh root@%s 'chmod 600 /var/spool/cron/work'" % host)
    print ret


def rsyncYzRedis(yzHostList):
  for yzHost in yzHostList:
    ret = commands.getoutput("rsync -avzp /home/work/CodisInstaller/deply_codis_yz/monitor root@%s:/home/work/opbin/" % yzHost)
    print ret
    ret = commands.getoutput("rsync -avzp /home/work/CodisInstaller/crontab_work root@%s:/var/spool/cron/work" % yzHost)
    print ret
    ret = commands.getoutput("rsync -avzp /home/work/CodisInstaller/deply_codis_xy/codis_6*  deply_codis_xy/codis_7* root@%s:/home/work/" % yzHost)
    print ret
    ret = commands.getoutput("rsync -avzp /home/work/CodisInstaller/deply_codis_yz/startCodis.sh root@%s:/home/work/" % yzHost)
    print ret

def createYzConfigini(codisName):
  ret = commands.getoutput("cp /home/work/CodisInstaller/config.ini.yz.template tmp/config.ini-%s" % codisName)
  print ret
  ret = commands.getoutput('sed -i "s#xxxx#%s#g" /home/work/CodisInstaller/tmp/config.ini-%s' % (codisName, codisName))
  print ret
  
def rsyncYzDashboard(yzHostList, codisName):
  for yzHost in yzHostList:
    ret = commands.getoutput("rsync -avzp /home/work/CodisInstaller/deply_codis_yz/dashboard root@%s:/home/work/" % yzHost)
    print ret
    ret = commands.getoutput("rsync /home/work/CodisInstaller/tmp/config.ini-%s root@%s:/home/work/dashboard/conf/config.ini" % (codisName, yzHost))
    print ret

def rsyncYzProxy(yzHostList, codisName):
  for yzHost in yzHostList:
    ret = commands.getoutput("rsync -avzp /home/work/CodisInstaller/deply_codis_yz/proxy_9100 root@%s:/home/work/" % yzHost)
    print ret
    ret = commands.getoutput("rsync /home/work/CodisInstaller/tmp/config.ini-%s root@%s:/home/work/proxy_9100/conf/config.ini" % (codisName, yzHost))
    print ret
    ret = commands.getoutput("rsync -avzp /home/work/CodisInstaller/deply_codis_yz/proxy_9200 root@%s:/home/work/" % yzHost)
    print ret
    ret = commands.getoutput("rsync /home/work/CodisInstaller/tmp/config.ini-%s root@%s:/home/work/proxy_9200/conf/config.ini" % (codisName, yzHost))
    print ret

def startYzDashboard(yzHostList):
  for yzHost in yzHostList:
    ret = commands.getoutput("ssh %s 'su - work -c \"source /etc/profile && cd /home/work/dashboard && sh load.sh start\"'" % yzHost)
    print ret

def startYzRedis(yzHostList):
  for yzHost in yzHostList:
    ret = commands.getoutput("ssh %s 'su - work -c \"source /etc/profile && for port in 6000 6001 6002 6003 6004 6005 7000 7001 7002 7003 7004 7005;do cd /home/work/codis_\$port && sh load.sh start;done\"'" % yzHost)
    print ret

def startYzProxy(yzHostList):
  for yzHost in yzHostList:
    ret = commands.getoutput("ssh %s 'su - work -c \"source /etc/profile && cd /home/work/proxy_9100 && sh load.sh start\"'" % yzHost)
    print ret
    ret = commands.getoutput("ssh %s 'su - work -c \"source /etc/profile && cd /home/work/proxy_9200 && sh load.sh start\"'" % yzHost)
    print ret

def createSh(codisName, yzHostList):
  codisServerAdd = "./bin/codis-config -c conf/config.ini server add %d %s:%d %s %s\n"
  codisSlotsInit = "./bin/codis-config -c conf/config.ini slot init\n"
  codisSlotsSet  = "./bin/codis-config -c conf/config.ini slot range-set %d %d %d online\n"
  masterList = [6000,6001,6002,6003,6004,6005]
  slaveList = [6000,6001,6002,6003,6004,6005]
  shellFileName = "/home/work/CodisInstaller/tmp/" + codisName + ".sh"
  with open(shellFileName, "w") as shellFile:
    shellFile.write("./bin/codis-config -c conf/config.ini config putidc yz rw\n")
    maxGroupNo = 0
    for indexHost, yzHost in enumerate(yzHostList):
      for indexMaster, master in enumerate(masterList):
        groupNo = indexHost*len(masterList)+indexMaster + 1
        maxGroupNo = groupNo 
        shellFile.write(codisServerAdd%(groupNo, yzHost, master, "master", "yz"))
        slaveHost = ""
        if indexHost >= len(yzHostList)-1:
          slaveHost = yzHostList[0]
        else:
          slaveHost = yzHostList[indexHost+1]
        shellFile.write(codisServerAdd%(groupNo, slaveHost, master+1000, "slave", "yz"))
        shellFile.write("sleep 1\n")
    
    shellFile.write(codisSlotsInit)
    shellFile.write("sleep 1\n")

    groupNum = len(yzHostList)*len(masterList)
    slotStep = int(1024/groupNum)
    end = -1
    for groupNo in range(1, groupNum+1):
      start = end + 1
      end = start + slotStep - 1
      end = min(end, 1023)
      shellFile.write(codisSlotsSet%(start, end, groupNo))
      shellFile.write("sleep 1\n")
    if end < 1023:
      groupNo = 1
      for slotNo in range(end+1, 1024):
        shellFile.write(codisSlotsSet%(slotNo, slotNo, groupNo))
        shellFile.write("sleep 1\n")
        groupNo += 1 
    shellFile.write("sleep 5\n") 
    shellFile.write("./bin/codis-config -c conf/config.ini config haturnon\n")
  
  ret = commands.getoutput("chown work:work %s" % shellFileName)
  print ret
  ret = commands.getoutput("su work -c 'scp %s %s:/home/work/dashboard/'" % (shellFileName, yzHostList[0]))
  print ret

def initCodis(codisName, host):
  ret = commands.getoutput("su work -c 'ssh %s \"source /etc/profile && cd /home/work/dashboard && sh %s.sh\"'" % (host, codisName))
  print ret

def main():
  if len(sys.argv) != 3:
    Usage()
    exit()

  codisName = sys.argv[1]
  if not codisName.endswith("-cache"):
    codisName += "-cache"
  yzHosts = sys.argv[2]

  yzHostList = yzHosts.split(",")
  for index, yzHost in enumerate(yzHostList):
    yzHostList[index] = yzHost.strip()

  check(codisName, yzHostList)

  confirm = raw_input("are you sure?[y/n]:")
  if confirm != 'y' and confirm != 'Y':
    exit()

  for index, yzHost in enumerate(yzHostList):
    hostName = "cds-" + codisName + "0" + str(index) + ".yz"
    changeHostName(yzHost, hostName)

  print "--------------------------->rsyncYzRedis"
  rsyncYzRedis(yzHostList)
  print "--------------------------->createYzConfigini"
  createYzConfigini(codisName)
  print "--------------------------->rsyncYzDashboard"
  rsyncYzDashboard(yzHostList, codisName)
  print "--------------------------->rsyncYzProxy"
  rsyncYzProxy(yzHostList, codisName)
  print "--------------------------->chown yz"
  chown(yzHostList)
  print "--------------------------->startYzRedis"
  startYzRedis(yzHostList)
  print "--------------------------->createSh"
  createSh(codisName, yzHostList)
  print "--------------------------->startYzDashboard"
  startYzDashboard(yzHostList)
  print "--------------------------->initCodis"
  time.sleep(2)
  initCodis(codisName, yzHostList[0])
  print "--------------------------->startYzProxy"
  startYzProxy(yzHostList)
  print "--------------------------->OK"


if __name__ == "__main__":
  main()
