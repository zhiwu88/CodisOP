#!/usr/bin/env python

import sqlite3
import commands

conn = sqlite3.connect('/home/work/CodisCenter/rsynccml/ClusterManager.db')
cursor = None
cursor = conn.execute('select hostname,ip from hostinfo order by hostname ASC')
class Host:
  def __init__(self):
    pass

hostlist = []
for row in cursor:
  host = Host()
  host.hostname = row[0]
  host.ip = row[1]
  hostlist.append(host)

conn.close()

insertSQL = 'insert into codisapp_hostinfo("HostIP", "HostName", "HostMem", "Room", "Description", "Used") values("%s", "%s", %d, "%s", "", 1)'

conn = sqlite3.connect('/home/work/CodisCenter/CodisCenter.db')
conn.execute('delete from codisapp_hostinfo')
for host in hostlist:
  hostname = host.hostname
  hostip = host.ip
  room = ''
  if hostname.endswith("xy"):
    room = "xy"
  elif hostname.endswith("yz"):
    room = "yz"
  else:
    room = "sz"
  ret = commands.getoutput("ssh %s 'free -g' | grep Mem | awk '{print $2}'" % hostip)
  mem = str(ret.split('\n')[1])
  conn.execute(insertSQL % (hostip, hostname, int(mem), room))

conn.commit()  
conn.close()
