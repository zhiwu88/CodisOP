#!/usr/bin/python

import redis
import time
import urllib2
import json
import sqlite3

#productDict = {
#                 "payui":"10.0.0.11", 
#                 "friend":"10.0.0.15",
#                 "hadoop":"10.0.0.1",
#                 "hb":"10.0.0.21",
#                 "hundred":"10.0.0.5",
#                 "jiaoyi":"10.0.0.17",
#                 "linkface":"10.0.0.13",
#                 "public":"10.0.0.1",
#                 "repayment":"10.0.0.20",
#                 "coupon":"10.0.0.7",
#                 "api":"10.0.0.5",
#                 "notice":"10.0.0.11",
#                 "reward":"10.0.0.9",
#                 "ermas":"10.0.0.8",
#                 "feed":"10.0.0.19",
#                 "huodong":"10.0.0.13",
#                 "payaccount":"10.0.0.17",
#                 "inner":"10.0.0.1",
#                 "cuiji":"10.0.0.4",
#                 "zhifu":"10.0.0.6",
#              }

productDict = {}
conn = sqlite3.connect("/home/work/CodisCenter/CodisCenter.db")
cursor = None
cursor = conn.execute('select ProductName, Dashboard from codisapp_codisinfo order by CodisID ASC')
for row in cursor:
  productDict[row[0]] = row[1]
conn.close()

conn = redis.Redis("127.0.0.1", 6000)

t = time.strftime("%Y-%m-%d",time.localtime(time.time() ))
key = "counter_" + t
ret = conn.expire(key, 3600*24*8)
  
for product, IP in productDict.items():
  url = "http://" + IP + "/api/overview"
  response = urllib2.urlopen(url)
  strret = response.read()
  info = json.loads(strret) 
  
  totalUsedMem = 0
  for redisInfo in info["redis_infos"]:
    mem = redisInfo["used_memory"]
    totalUsedMem += long(mem)
  
  mem = int(totalUsedMem/1024/1024/1024)
  #if product == "coupon":
  #  mem -= 11
  #if product == "payui":
  #  mem -= 12
  #if product == "hb":
  #  mem -= 11
  #if product == "linkface":
  #  mem -= 11
  mem = str(mem)


  ret = conn.hset(key, product, mem)
  
ret = conn.expire(key, 3600*24*8)
