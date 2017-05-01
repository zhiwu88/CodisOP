#!/usr/bin/env python

import redis
import pp
import urllib2
import json
import time
import sqlite3

def get(url):
  response = urllib2.urlopen(url)
  data = response.read()
  ret = json.loads(data)
  return ret

def scan(addr, productName):
  connResult = redis.Redis("100.0.0.1", 6000)
  IP = addr.split(':')[0]
  Port = int(addr.split(':')[1])
  conn = redis.Redis(IP, Port)
  cursor = 0
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
            connResult.zadd("BigKey_" + productName, key, int(ret['serializedlength']))
            idletime = int(ret['lru_seconds_idle'])
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()-idletime))
            connResult.setex(productName+"_"+key, t, 3600*24)
            #keytype = conn.type(key)
            #connResult.setex(productName+"_"+key+"_type", keytype, 3600*24)
            
            #t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            #connResult.set("BigKey_" + productName + "_time", t)
            #print "key=" + keys[index] + ",length=" + str(ret['serializedlength'])

    if cursor == 0:
      break

def CodisScan(IP, productName):
  url = "http://" + IP + "/api/server_groups"
  groups = get(url)
  slaves = []
  #t1 = time.time()
  for group in groups:
    for server in group["servers"]:
      if server["type"] == "slave" and server["addr"].startswith("10.0"): 
        slaves.append(server["addr"])

  #ppservers = ("100.0.0.2:35000", "100.0.0.3:35000", "100.0.0.4:35000")
  ppservers = ()
  job_server = pp.Server(20, ppservers=ppservers, secret="worker")
  jobs = [(job_server.submit(scan, (slave, productName), (), ("redis","time","json",))) for slave in slaves]
  for job in jobs:
    job()
     
  status = job_server.get_stats()
  job_server.destroy()
  #t2 = time.time()
  #print "time=" + str(int(t2-t1))

def main():
  productDict = {}
  conn = sqlite3.connect("/home/work/CodisCenter/CodisCenter.db")
  cursor = None
  cursor = conn.execute('select ProductName, Dashboard from codisapp_codisinfo order by CodisID ASC')
  for row in cursor:
    productDict[row[0]] = row[1]
  conn.close() 
  #productDict = {
  #               "payui":"10.0.0.11",
  #               "friend":"10.0.0.15",
  #               "hadoop":"10.0.0.1",
  #               "hb":"10.0.0.21",
  #               "hundred":"10.0.0.5",
  #               "jiaoyi":"10.0.0.17",
  #               "linkface":"10.0.0.13",
  #               "public":"10.0.0.1",
  #               "repayment":"10.0.0.20",
  #               "coupon":"10.0.0.7",
  #               "api":"10.0.0.5",
  #               "notice":"10.0.0.11",
  #               "reward":"10.0.0.9",
  #               #"ermas":"10.0.0.8",
  #               "feed":"10.0.0.19",
  #               "huodong":"10.0.0.13",
  #               "inner":"10.0.0.1",
  #               "payaccount":"10.0.0.17",
  #            } 
  conn = redis.Redis("100.0.0.1", 6000)
  while True:
    t1 = time.time()
    for productName, IP in productDict.items():
      tstart = time.time()
      t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
      print "start:" + t + ",",
      
      print "-->" + productName
      conn.delete("BigKey_" + productName)
      conn.delete("BigKey_" + productName + "_time")
      CodisScan(IP, productName)
      tend = time.time()
      print "end-->" + productName + ", t=" + str(int(tend-tstart))
      t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
      conn.set("BigKey_" + productName + "_time", t)
      
    t2 = time.time()
    print "time=" + str(t2-t1)

if __name__ == "__main__":
  main()

