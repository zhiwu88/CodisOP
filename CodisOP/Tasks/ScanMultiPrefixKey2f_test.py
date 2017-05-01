#!/usr/bin/env python

import redis
import urllib2
import json
import time

start_time = time.time()

def get(url):
  response = urllib2.urlopen(url)
  data = response.read()
  ret = json.loads(data)
  return ret


groupsurl = "http://100.0.0.1:8080/api/server_groups"
groups = get(groupsurl)
for group in groups:
  slave = ""
  for server in group["servers"]:
    if server["type"] == "slave":
      slave = server["addr"]
      break
  if slave != "":
    redisIP = slave.split(":")[0]
    redisPort = int(slave.split(":")[1])
    conn = redis.Redis(redisIP, redisPort)
    cursor = 0
    with open("ScanMultiPrefixKey2f_test.txt", "a") as f:
      while True:
        cursor, keys = conn.scan(cursor, count=10000)
        for key in keys:
          if key.startswith("keykey11111111") or key.startswith("keykey11111112"):
            print key
            f.write(key + '\n')
        if 0 == cursor:
          break

end_time = time.time()
print("done: %f s" % (end_time - start_time))