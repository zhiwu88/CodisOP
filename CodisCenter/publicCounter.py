#!/usr/bin/env python
# -*- encoding:utf-8 -*-

'''统计public集群的各个前缀对应的key的数量'''

import thread
import sys
from kazoo.client import KazooClient
import redis
import time
import json
import threading
import copy
import urllib2, base64
import socket, fcntl, struct
import socket
import sqlite3
reload(sys)
sys.setdefaultencoding('utf8')

zkAddr = "10.0.0.2:2181"

productName = "rrx-public-cache"

prefixList = []

prefixCounter = {}

NoPrefix = 0

def ScanCodisServer(IP, Port, f):
  global prefixCounter 
  global NoPrefix
  conn = redis.Redis(IP, Port)
  cursor = 0
  while True:
    cursor, keys = conn.scan(cursor, count=10000)
    with conn.pipeline() as p:
      for key in keys:
        p.debug_object(key)
      rets = p.execute(raise_on_error=False)
      for index, ret in enumerate(rets):
        ifFind = False
        #print keys[index]
        keys[index] = keys[index].decode('utf8', "ignore")
        for prefix in prefixCounter:
          if str(keys[index]).startswith(prefix):
            if isinstance(ret, dict) and ret.has_key('serializedlength'):
              prefixCounter[prefix][0] += 1
              prefixCounter[prefix][1] += ret['serializedlength']
            ifFind = True
            break
        if not ifFind:
          NoPrefix += 1
          f.write(keys[index] + "\n")
      
    if 0 == cursor:
      return 

def get(url):
  response = urllib2.urlopen(url)
  data = response.read()
  ret = json.loads(data)
  return ret

def GetSlaveList():
  slaveList = []  

  url = "http://10.0.0.1:8080/api/server_groups"
  groups = get(url)

  for group in groups:
    for server in group["servers"]:
      if server["type"] == "slave" and server["addr"].startswith("10.0"):
        slaveList.append(server["addr"])

  return slaveList

def main():
  global prefixCounter
  global prefixList
  conn = sqlite3.connect("/home/work/CodisCenter/CodisCenter.db") 
  cursor = None
  cursor = conn.execute('select PrefixName from codisapp_publicprefix order by PrefixID ASC') 
  for row in cursor:
    prefixCounter[row[0]] = [0, 0] 
    prefixList.append(row[0])
  conn.close()

  with open("/home/work/CodisCenter/public_noprefix.log", "w") as f:
    slaveList = GetSlaveList()
    for slave in slaveList:
      slaveIP = slave.split(":")[0]
      slavePort = int(slave.split(":")[1])
      t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
      print str(slave) + "-->starttime:" + str(t)
      ScanCodisServer(slaveIP, slavePort, f)
      t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
      print str(slave) + "-->endtime:" + str(t)

  conn = redis.Redis("127.0.0.1", 6000)
  for prefix in prefixList:
    ret = conn.hset("public_keynum", prefix, str(prefixCounter[prefix][0]))
    ret = conn.hset("public_keymem", prefix, str(prefixCounter[prefix][1]))
  
  ret = conn.set("public_noprefix", str(NoPrefix))
  t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
  ret = conn.set("public_counter_time", t)

  print prefixCounter

if __name__ == "__main__":
  start = time.time()
  main()
  end = time.time()
  print "time=" + str(end-start)
