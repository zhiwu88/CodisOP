#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import commands
import urllib2
import redis
import time
import json
import sys
import os
import sqlite3

productList = []
productDict = {}
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
#
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
#                 "inner":"10.0.0.1",
#                 "payaccount":"10.0.0.17",
#                 "cuiji":"10.0.0.4",
#                 "zhifu":"10.0.0.6",
#              }


autoaofCommand="echo 'config set auto-aof-rewrite-percentage 0' | ./redis-cli -h %s -p %d && echo 'config rewrite' | ./redis-cli -h %s -p %d"
backlogCommand="echo 'config set repl-backlog-size 1073741824' | ./redis-cli -h %s -p %d && echo 'config rewrite' | ./redis-cli -h %s -p %d"

def get(url):
  response = urllib2.urlopen(url) 
  data = response.read()
  ret = json.loads(data)
  return ret

def printMsg(productName, groupID, Msg):
  print "[ERROR]groupID=" + str(groupID) + ": " + Msg
  
def checkProxy(proxys):
  for proxy in proxys:
    if proxy['state'] != "online":
      print "[ERROR]proxy offline!proxy=" + proxy['addr']
    ip = proxy['addr'].split(':')[0] 
    port = int(proxy['addr'].split(':')[1])
    conn = redis.Redis(ip, port)
    if not conn.info().has_key('used_memory'):
      print "proxy:" + proxy['addr'] + "-> connnect get info error"

def checkRedis(master, xyslave, yzslave, productName):
  masterConn = redis.Redis(master.split(":")[0], int(master.split(":")[1]))
  xyslaveConn = redis.Redis(xyslave.split(":")[0], int(xyslave.split(":")[1])) 
  yzslaveConn = redis.Redis(yzslave.split(":")[0], int(yzslave.split(":")[1])) 

  try:
    masterInfo = masterConn.info()
  except redis.exceptions.ConnectionError as e:
    print master + " connection refrused" 
    return
  try:
    xyslaveInfo = xyslaveConn.info()
  except redis.exceptions.ConnectionError as e:
    print xyslave + " connection refrused" 
    return 

  try:
    yzslaveInfo = yzslaveConn.info()
  except redis.exceptions.ConnectionError as e:
    print yzslave + " connection refrused" 
    return

  if masterInfo['role'] != 'master':
    print "master:" + master + "->info[role] != master"
  if masterInfo['connected_slaves'] != 3:
    print "master:" + master + "->info[connected_slaves] != 3" 
  if masterInfo['connected_slaves'] == 2:
    slave0 = masterInfo['slave0']['ip'] + ":" + str(masterInfo['slave0']['port'])
    slave1 = masterInfo['slave1']['ip'] + ":" + str(masterInfo['slave1']['port'])
    if slave0 != xyslave and slave0 != yzslave:
      print "slave0:" + slave0 + "-> != codis.info"
    if slave1 != xyslave and slave1 != yzslave:
      print "slave1:" + slave1 + "-> != codis.info"
    if masterInfo['slave0']['state'] != 'online' or long(masterInfo['slave0']['offset']) <= 0:
      print "slave0:" + slave0 + " state not ready!"
      print masterInfo['slave0']
    if masterInfo['slave1']['state'] != 'online' or long(masterInfo['slave1']['offset']) <= 0:
      print "slave1:" + slave1 + " state not ready!"
      print masterInfo['slave1']
  if xyslaveInfo['role'] != 'slave':
    print "xyslave:" + xyslave + "->info[role] != slave"
  if yzslaveInfo['role'] != 'slave':
    print "yzslave:" + yzslave + "->info[role] != slave"
  
  
  if masterInfo['mem_fragmentation_ratio'] > 1.3 and masterInfo['used_memory'] > 5368709120:
    print master + ": fragmentation=" + str(masterInfo['mem_fragmentation_ratio']) + "! " 
  if xyslaveInfo['mem_fragmentation_ratio'] > 1.3 and xyslaveInfo['used_memory'] > 5368709120:
    print xyslave + ": fragmentation=" + str(xyslaveInfo['mem_fragmentation_ratio']) + "! " 
  if yzslaveInfo['mem_fragmentation_ratio'] > 1.3 and yzslaveInfo['used_memory'] > 5368709120:
    print yzslave + ": fragmentation=" + str(yzslaveInfo['mem_fragmentation_ratio']) + "! "

def checkUsedMemory(masters):
  usedMemory = 0L
  for master in masters:
    masterConn = redis.Redis(master.split(":")[0], int(master.split(":")[1]))  
    masterInfo = masterConn.info()
    if usedMemory == 0:
      usedMemory = long(masterInfo['used_memory'])
    elif long(masterInfo['used_memory']) > usedMemory*1.3 and usedMemory > 0:
      print master + " used_memory is bigger!"
    #elif usedMemory > long(masterInfo['used_memory'])*1.3 and usedMemory > 0:
    #  print "masterInfo['used_memory']="+str(masterInfo['used_memory'])
    #  print "usedMemory=" + str(usedMemory)
    #  print masters[0] + " used_memory is bigger!"
     

def checkGroups(groups):
  maxmemory = 0
  masters = []
  for group in groups:
    master = ""
    xyslave = ""
    yzslave = ""
    productName = group["product_name"]
    groupID = group["id"]
    for server in group["servers"]:
      if server["type"] == "master":
        master = server["addr"]
        masters.append(master)
      elif server["type"] == "slave":
        if server["addr"].startswith("10.0") or server["addr"].startswith("100.0"):
          xyslave = server["addr"]
        else:
          yzslave = server["addr"]
      
      if server["addr"] != "":    
        redisIP = server["addr"].split(":")[0]
        redisPort = int(server["addr"].split(":")[1])
        conn = redis.Redis(redisIP, redisPort) 
        try:
          connret = conn.ping()
          current_config = conn.config_get()
          repl_backlog_size = int(current_config['repl-backlog-size'])
          redismaxmemory = int(current_config['maxmemory'])
          auto_aof_rewrite_percentage = int(current_config['auto-aof-rewrite-percentage'])
          
          if repl_backlog_size != 1073741824:
            printMsg(productName, groupID, server["addr"]+" repl-backlog-size != 1073741824") 
            #ret = commands.getoutput(backlogCommand%(redisIP, redisPort, redisIP, redisPort))
            #print "repl-backlog-size--->" + ret
          if auto_aof_rewrite_percentage != 0:
            printMsg(productName, groupID, server["addr"]+" auto-aof-rewrite-percentage != 0") 
            #ret = commands.getoutput(autoaofCommand%(redisIP, redisPort, redisIP, redisPort))
            #print "auto-aof-rewrite-percentage--->" + ret
          if maxmemory == 0:
            maxmemory = redismaxmemory
          elif redismaxmemory != maxmemory:
            printMsg(productName, groupID, server["addr"]+" redismaxmemory=" + str(redismaxmemory)) 
        except redis.exceptions.ConnectionError as e:
          printMsg(productName, groupID, server["addr"] + str(e)) 
          
        
    
    if master == "":
      printMsg(productName, groupID, "master = ''")
    if xyslave == "" and productName != "rrx-ermas-cache":
      printMsg(productName, groupID, "xyslave = ''")
    if yzslave == "" and productName.find("inner") < 0:
      printMsg(productName, groupID, "yzslave = ''")
    if (master != "") and ((not master.startswith("10.0.") and not master.startswith("100.0.")) or (not master.split(":")[1].startswith("600"))):
      printMsg(productName, groupID, "master warn!!! master=" + master)
    if (xyslave != "") and ((not xyslave.startswith("10.0.") and not xyslave.startswith("100.0.")) or (not xyslave.split(":")[1].startswith("700"))):
      printMsg(productName, groupID, "xyslave warn!!! xyslave=" + xyslave)
    if (yzslave != "") and ((not yzslave.startswith("100.")) or (not (yzslave.split(":")[1].startswith("600") or yzslave.split(":")[1].startswith("700")))):
      if productName.find("inner") < 0:
        printMsg(productName, groupID, "yzslave warn!!! yzslave=" + yzslave)
    
    if productName != "rrx-ermas-cache":
      if master != "" and xyslave != "" and yzslave != "":
        checkRedis(master, xyslave, yzslave, productName)
  checkUsedMemory(masters)

def checkHa(dashboard):
  url = "http://" + dashboard + "/api/ha"
  ha = get(url)
  if ha["ha"] != "On":
    print "[ERROR]ha off!"

def Usage():
  print '''
Usage:
     ck productName
     or
     ck all

'''

    
def main():
  global command
  global productList
  global productDict

  conn = sqlite3.connect("/home/work/CodisCenter/CodisCenter.db")
  cursor = None
  cursor = conn.execute('select ProductName, Dashboard from codisapp_codisinfo order by CodisID ASC')
  for row in cursor:
    productList.append(row[0])
    productDict[row[0]] = row[1]
  conn.close()

  if len(sys.argv) < 2:
    Usage()
    exit()
  
  if sys.argv[1] == "all":
    for product in productList:
      IP = productDict[product]
      #print IP
      dashboard = "http://" + IP 
      groupsurl = dashboard + "/api/server_groups"
      groups = get(groupsurl)
      
      #print "=======%s========" % product
      checkGroups(groups)
      time.sleep(1)
      #print "========end===========\n"
     
      proxysurl = dashboard + "/api/proxy/list"
      proxys = get(proxysurl)
      checkProxy(proxys)
      checkHa(IP)
  else:
    product = sys.argv[1]
    IP = productDict[product]
    #print IP
    dashboard = "http://" + IP 
    groupsurl = dashboard + "/api/server_groups"
    groups = get(groupsurl)
    
    #print "=======%s========" % product
    checkGroups(groups)
    #print "========end==========\n"
    
    proxysurl = dashboard + "/api/proxy/list"
    proxys = get(proxysurl)
    checkProxy(proxys)
    checkHa(IP)

if __name__ == "__main__":
  main()
