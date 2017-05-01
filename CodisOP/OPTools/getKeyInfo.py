#!/usr/bin/env python

import sys
import sqlite3
import time
import redis
import binascii
import urllib2
import json

def Usage():
  print '''
Usage:
    python keyinfo.py codisname key
'''

def GetDashboard(codisname):
  conn = sqlite3.connect("/home/work/CodisInstaller/tools/ClusterManager/ClusterManager.db")
  cursor = None
  cursor = conn.execute('select ip from hostinfo where hostname like "%' + codisname + '%.xy" order by hostname ASC')
  ip = ""
  for row in cursor:
    ip = row[0]
    break
  conn.close() 
  return ip

def get(url):
  response = urllib2.urlopen(url)
  data = response.read()
  ret = json.loads(data)
  return ret
  
def GetSlotNo(key):
  crc32value = binascii.crc32(key)
  slotNo = crc32value % 1024
  return slotNo  

def GetGroupNo(slots, slotNo):
  for slot in slots:
    if slot["id"] == slotNo:
      return slot["group_id"]
  return -1

def main():
  if len(sys.argv) < 3:
    Usage()
    exit()

  codisname = sys.argv[1]
  key = sys.argv[2]
  ip = GetDashboard(codisname)
  url = "http://" + ip + ":8080/api/slots/"
  slots = get(url)
  slotNo = GetSlotNo(key)
  groupNo = GetGroupNo(slots, slotNo)
  url = "http://" + ip + ":8080/api/server_groups/"
  groups = get(url)
  master = ""
  xyslave = ""
  yzslave = ""
  for group in groups:
    if group["id"] == groupNo:
      for server in group["servers"]:
        if server["type"] == "master":
          master = server["addr"]
        if server["type"] == "slave" and server["addr"].startswith("10.0"):
          xyslave = server["addr"]
        if server["type"] == "slave" and server["addr"].startswith("100."):
          yzslave = server["addr"]

  length = ""
  t = ""
  exists = True
  if xyslave != "":
    conn = redis.Redis(xyslave.split(":")[0], int(xyslave.split(":")[1]))
    try:
      if not conn.exists(key):
        exists = False
      else:
        ret = conn.debug_object(key)
        if isinstance(ret, dict) and ret.has_key('serializedlength'):
          length = int(ret['serializedlength'])
          idletime = int(ret['lru_seconds_idle'])  
          t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()-idletime))
    except redis.exceptions.ResponseError as e:
      exists = False

  if not exists:
    print "no this key"
    return
  else:
    print "---------------------------------"
    print "key=" + key
    print "codis=" + codisname
    print "dashboard=" + ip + ":8080"
    print "slotNo=" + str(slotNo)
    print "groupNo=" + str(groupNo)
    print "master=" + master
    print "xyslave=" + xyslave
    print "yzslave=" + yzslave
    print "length=" + str(length)
    print "last access=" + t
    print "---------------------------------"

if __name__ == '__main__':
  main()
