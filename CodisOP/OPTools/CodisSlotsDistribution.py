#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import sys

masterList = [6000,6001,6002,6003,6004,6005]

startGroupNo = 0

def Usage():
  print ''' Usage:
    python CodisSlotsDistribution.py productName.sh 10.0.0.6,10.0.0.7'''

def main():
  if len(sys.argv) < 3:
    Usage()
    exit()

  codisServerAdd = "./bin/codis-config -c conf/config.ini server add %d %s:%d %s %s\n"
  codisSlotsInit = "./bin/codis-config -c conf/config.ini slot init\n"
  codisSlotsSet  = "./bin/codis-config -c conf/config.ini slot range-set %d %d %d online\n"

  shellFileName = sys.argv[1]
  hostList = (sys.argv[2]).split(",")  
  
  with open(shellFileName, "w") as shellFile:
    for indexHost, host in enumerate(hostList):
      for indexMaster, master in enumerate(masterList):
        groupNo = indexHost*len(masterList)+indexMaster+1 + startGroupNo
        shellFile.write(codisServerAdd%(groupNo, host, master, "master", "xy"))
        slaveHost = ""
        if indexHost >= len(hostList)-1:
          slaveHost = hostList[0]
        else:
          slaveHost = hostList[indexHost+1]
        shellFile.write(codisServerAdd%(groupNo, slaveHost, master+1000, "slave", "xy"))
        shellFile.write("sleep 1\n")

    shellFile.write(codisSlotsInit)
  
    groupNum = len(hostList)*len(masterList)
    slotStep = int(1024/groupNum)
    end = -1
    for groupNo in range(1, groupNum+1):
      start = end + 1
      end = start + slotStep - 1
      end = min(end, 1023)
      shellFile.write(codisSlotsSet%(start, end, groupNo))
      shellFile.write("sleep 1\n")
    if end < 1023:
      groupNo = 1
      for slotNo in range(end+1, 1024):
        shellFile.write(codisSlotsSet%(slotNo, slotNo, groupNo))
        shellFile.write("sleep 1\n")
        groupNo += 1
        
  
if __name__ == "__main__":
  main()
