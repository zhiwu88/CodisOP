#!/usr/bin/env python

import commands
import urllib2
import json
import sys
from pprint import pprint

IP = "100.107.11.1"
url = "http://" + IP + ":8080/api/overview"
#print url
response = urllib2.urlopen(url)
strret = response.read()
info = json.loads(strret)
#pprint (info)

IPSet = set([])
totalKeyNum = 0
totalMem = 0
for redisInfo in info["redis_infos"]:
    keyNum = redisInfo["db0"].split(",")[0].split("=")[1]
    totalKeyNum += int(keyNum)
    mem = redisInfo["used_memory"]
    totalMem += long(mem)
    IPSet.add(redisInfo["slave0"].split(",")[0].split("=")[1])
    IPSet.add(redisInfo["slave1"].split(",")[0].split("=")[1])
    IPSet.add(redisInfo["slave2"].split(",")[0].split("=")[1])

maxMem = info["maxmemory"]

print IP + "\t" + str(totalKeyNum) + "\t" + str(totalMem/1024/1024/1024) + "\t" + str(maxMem)
print IPSet
print "IP address Numbers is:", len(IPSet)

