#!/usr/bin/env python

import redis
import urllib2
import json
import time

def get(url):
    response = urllib2.urlopen(url)
    data = response.read()
    rst = json.loads(data)
    return rst

cmd_promote = "./bin/codis-config -c conf/config.ini server promote %s %s\n"
sleep_time = "sleep 30\n"

groupsurl = "http://10.0.0.5:8080/api/server_groups"
groups = get(groupsurl)

with open('promote_master.txt', 'w') as outFile:
    for group in groups:
        gid = group["id"]
        for server in group["servers"]:
            if server["type"] == "slave" and server["idc"] == "xy":
                slaveaddr = server["addr"]
                outFile.write(cmd_promote %(gid ,slaveaddr))
        outFile.write(sleep_time)
