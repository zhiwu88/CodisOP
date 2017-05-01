#!/usr/bin/env python

import redis
import urllib2
import json
import time
import sqlite3

productDict = { "test":"10.0.0.5" } 

def get(url):
  response = urllib2.urlopen(url)
  data = response.read()
  ret = json.loads(data)
  return ret

def scan(addr, productName):
  IP = addr.split(':')[0]
  Port = int(addr.split(':')[1])
  conn = redis.Redis(IP, Port)
  cursor = 0
  with open("ScanBigKeyInCluster2f.txt", "a") as f:
    while True:
      cursor, keys = conn.scan(cursor, count=10000)
      with conn.pipeline() as p:
        for key in keys:
          p.debug_object(key)
        rets = p.execute(raise_on_error=False)
        for index, ret in enumerate(rets):
          if not isinstance(ret, redis.exceptions.ResponseError):
            if ret['serializedlength'] > 1024*1024 or ret['serializedlength'] < 0:
              key = keys[index]
              idletime = int(ret['lru_seconds_idle'])
              t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()-idletime))
              print "key='" + key +"' lastAccess='" + t + "t"  + " 'serializedlength='" + str(ret['serializedlength'])
              f.write("key='" + key +"' lastAccess='" + t + "t"  + " 'serializedlength='" + str(ret['serializedlength']) + '\n')

      if cursor == 0:
        break

def CodisScan(IP, productName):
  url = "http://" + IP + ":8080/api/server_groups"
  groups = get(url)
  slaves = []
  #t1 = time.time()
  for group in groups:
    for server in group["servers"]:
      if server["type"] == "slave" and server["addr"].startswith("10.0"): 
        slaves.append(server["addr"])

  for slave in slaves:
    scan(slave, productName)


def main():
  global productDict 
  t1 = time.time()
  for productName, IP in productDict.items():
    tstart = time.time()
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print "start:" + t + ",",
    
    print "-->" + productName
    CodisScan(IP, productName)
    tend = time.time()
    print "end-->" + productName + ", t=" + str(int(tend-tstart))
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
  t2 = time.time()
  print "time=" + str(t2-t1)

if __name__ == "__main__":
  main()

