#!/usr/bin/env python

import redis
import urllib2
import json
import time
import sqlite3

productDict = { "notice":"100.0.0.5" } 

totalNum = 0
totalMem = 0

prefixmap = {}

def get(url):
  response = urllib2.urlopen(url)
  data = response.read()
  ret = json.loads(data)
  return ret

def scan(addr, productName):
  global totalNum
  global totalMem
  global prefixmap
  
  prefixList = ['NOTICE_USER_INFO','NOTICE_P','NOTICE_PUSH_DATA','NOTICE_DEVICE_INFO','NOTICE_BADGE_NUM','NOTICE_MI_INVALID_TOKEN','NOTICE_GLOBAL_TIPS','NOTICE_USER_TIPS','NOTICE_USER_SWITCH']
  

  IP = addr.split(':')[0]
  Port = int(addr.split(':')[1])
  conn = redis.Redis(IP, Port)
  cursor = 0
  while True:
    cursor, keys = conn.scan(cursor, count=10000)
    for key in keys:
      iffound = False
      for prefix in prefixList:
        if key.startswith(prefix):
          if prefixmap.has_key(prefix):
            prefixmap[prefix] = prefixmap[prefix] + 1
          else:
            prefixmap[prefix] = 1
          iffound = True
          break
      if not iffound:
        print key

    if cursor == 0:
      break

def CodisScan(IP, productName):
  url = "http://" + IP + ":8080/api/server_groups"
  groups = get(url)
  slaves = []
  #t1 = time.time()
  for group in groups:
    for server in group["servers"]:
      if server["type"] == "slave" and server["addr"].startswith("100."): 
        slaves.append(server["addr"])
        break

  for slave in slaves:
    print slave
    scan(slave, productName)


def main():
  global productDict 
  global totalNum

  for productName, IP in productDict.items():
    CodisScan(IP, productName)

  print prefixmap
    

if __name__ == "__main__":
  main()

