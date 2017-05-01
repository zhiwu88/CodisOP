#!/usr/bin/env python

import json
import urllib2
import sys
from pprint import pprint
import math

def Usage():
  print '''
Usage:
    python MigrateSlots.py IP
'''

def getGid(IP):
    GroupAPI = "http://" + IP + ":8080/api/server_groups"
    print "Group API:", GroupAPI
    response = urllib2.urlopen(GroupAPI)
    page_str = response.read()
    group_json_list = json.loads(page_str)
    GidList = []
    for group in group_json_list:
        for server in group["servers"]:
            #pprint(server)
            if server["type"] == "master" and server["addr"].split(':')[0] == IP:
                #pprint(server["group_id"])
                GidList.append(server["group_id"])
    return GidList


def getSlotID(IP, GidList):
    SlotAPI = "http://" + IP + ":8080/api/slots"
    print "Slot API:", SlotAPI
    response = urllib2.urlopen(SlotAPI)
    page_str = response.read()
    slot_json_list = json.loads(page_str)
    SlotList = []
    for slot in slot_json_list:
        #pprint(slot["id"])
        if slot["group_id"] in GidList:
            #print slot["group_id"], slot["id"]
            SlotList.append(slot["id"])
    return SlotList


def writeMigrateShell(IP, SlotList):
    slotsum = len(SlotList)
    print slotsum
    SlotList.sort()
    print SlotList
    rangeNum = math.ceil(slotsum//12)
    dstGid = 1
    with open("MigrateShell_" + IP, "w") as f:
        while (len(SlotList) > 0):
            index = 0
            while (index < rangeNum):
                #print dstGid, SlotList[0]
                f.write("bin/codis-config -c conf/config.ini slot migrate {0} {0} {1} \n".format(SlotList[0], dstGid))
                f.write("sleep 1 \n")
                SlotList.pop(0)
                index += 1
            if len(SlotList) < rangeNum:
                for Sid in SlotList:
                    #print dstGid, Sid
                    f.write("bin/codis-config -c conf/config.ini slot migrate {0} {0} {1} \n".format(Sid, dstGid))
                    f.write("sleep 1 \n")
            dstGid += 1
            if dstGid > 12:
                break



def main():
    IP = sys.argv[1]
    GidList = getGid(IP)
    print(GidList)
    SlotList = getSlotID(IP, GidList)
    print(SlotList)
    writeMigrateShell(IP, SlotList)


if __name__ == "__main__":
    main()

