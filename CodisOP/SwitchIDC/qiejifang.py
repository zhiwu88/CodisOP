#!/usr/bin/env python

import json
import urllib2
import redis
import sys


def get(url):
  response = urllib2.urlopen(url)
  data = response.read()
  ret = json.loads(data)
  return ret

def Usage():
  print '''
Usage:
    python qiejifang.py codisName dashboardIP
'''

def main():
  if len(sys.argv) != 3:
    Usage()
    exit()

  codisName = sys.argv[1]
  IP = sys.argv[2]

  PromoteCommand = "./bin/codis-config -c conf/config.ini server promote %d %s\n"

  dashboard = IP + ":8080"
  url = "http://" + dashboard + "/api/server_groups/"
  groups = get(url)

  with open("tmp/" + codisName + "-proYz.sh", "w") as yzFile:
    yzFile.write("./bin/codis-config -c conf/config.ini config putidc yz rw\n")
    for group in groups:
      for server in group["servers"]:
        if server["type"] == "slave" and server["addr"].startswith("100.") and server["addr"][0:-1].endswith("600"):
          yzFile.write(PromoteCommand % (server["group_id"], server["addr"]))


  with open("tmp/" + codisName + "-proXy.sh", "w") as xyFile:
    xyFile.write("./bin/codis-config -c conf/config.ini config putidc xy rw\n")
    for group in groups:
      for server in group["servers"]:
        if server["type"] == "master" and server["addr"].startswith("10.0") and server["addr"][0:-1].endswith("600"):
          xyFile.write(PromoteCommand % (server["group_id"], server["addr"]))





if __name__ == '__main__':
  main()
