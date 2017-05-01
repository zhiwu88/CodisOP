#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import redis
import sqlite3
import time
import commands

#productList = [
#                "hundred",
#                "hb",
#                "reward",
#                "notice",
#                "public",
#                "linkface",
#                "api",
#                "jiaoyi",
#                "friend",
#                "ermas",
#                "repayment",
#                "payui",
#                "coupon",
#                "feed",
#                "hadoop",
#                "huodong",
#                "inner",
#                "payaccount",
#                "cuiji",
#                "zhifu",
#              ]
productList = []
conn = sqlite3.connect("/home/work/CodisCenter/CodisCenter.db")
cursor = None
cursor = conn.execute('select ProductName from codisapp_codisinfo order by CodisID ASC')
for row in cursor:
  productList.append(row[0])
conn.close()
#print productList

command = "/usr/bin/python /home/work/CodisCenter/checkCodis.py %s"

conn = redis.Redis("127.0.0.1", 6000)

for product in productList:
  output = commands.getoutput(command % product)
  if output == "":
    ret = conn.hset("codis_monitor", product, "good")
  else:
    ret = conn.hset("codis_monitor", product, output)

t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
ret = conn.set("codis_monitor_time", t)
