#!/usr/bin/env python

import sys
import json
import time
import commands
import urllib2

# python CodisCommand.py info
# python CodisCommand.py "info stat"
# python CodisCommand.py "config get maxmemory"


def get(url):
  response = urllib2.urlopen(url)
  data = response.read()
  ret = json.loads(data)
  return ret

def execCommand(redisAddr, command):
  ip = redisAddr.split(":")[0]
  port = redisAddr.split(":")[1]
  output = commands.getoutput("echo '%s' | ./redis-cli -h %s -p %s" % (command, ip, port))
  print "=======%s======"%redisAddr
  print "=======%s======"%command
  print output
  print "=======end========"
  output = commands.getoutput("echo 'config rewrite' | ./redis-cli -h %s -p %s" % (ip, port))
  print "=======%s======"%redisAddr
  print "=======config rewrite======"
  print output
  print "=======end========"
  

def main():
  command = sys.argv[1]
  url = "http://100.107.11.1:8080/api/server_groups/"
  groups = get(url)
  for group in groups:
    for server in group["servers"]:
      execCommand(server["addr"], command)
  
if __name__ == "__main__":
  main()
