#!/usr/bin/python

import redis
import time

productDict = {
                 "payui":"3", 
                 "friend":"655",
                 "hadoop":"104",
                 "hb":"5",
                 "hundred":"114",
                 "jiaoyi":"39",
                 "linkface":"1",
                 "public":"45",
                 "repayment":"30",
                 "coupon":"1",
                 "api":"133",
                 "notice":"40",
                 "reward":"43",
                 "ermas":"294",
                 "feed":"148"
                }

conn = redis.Redis("127.0.0.1", 6000)

for i in range(7):
  t = time.strftime("%Y-%m-%d",time.localtime(time.time() - 3600*24*(i+1)))
  key = "counter_" + t
  
  for product, mem in productDict.items():
    ret = conn.hset(key, product, mem)
  
