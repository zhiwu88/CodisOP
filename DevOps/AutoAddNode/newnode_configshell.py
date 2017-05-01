import urllib2
import sys
import json
import sqlite3
from pprint import pprint

#python newnode_configshell.py t1

def getApiIP(codisName):
	cdscodisName = "cds-" + codisName
	conn = sqlite3.connect("/home/work/CodisInstall_YZ/ClusterManagerTest.db")
	cursor = conn.execute("select ip from hostinfo where hostname like ?", (cdscodisName + "__.yz%",))
	#iplistall = cursor.fetchall()
	#for i in iplistall:
	#	print i
        iplist = cursor.fetchone()
        #print iplist[0]
	return iplist[0]

def getInfo(ApiIP):
	APIURL = "http://" + ApiIP + ":8080/api/server_groups"
	print "Dashboard API:",APIURL
	response = urllib2.urlopen(APIURL)
	page_str = response.read()
	json_list = json.loads(page_str)
	#print json_list
	return json_list
	
def getMaxGID(groupsInfo):
	listID = []
	for group in groupsInfo:
		#print group["id"]
		listID.append(group["id"])
	print "Group ID has:", listID
	print "MAX GID is:", max(listID)
	return max(listID)

def configShell(codisName,yzHostList,newGid):
    print codisName,yzHostList,newGid
    codisServerAdd = "./bin/codis-config -c conf/config.ini server add %d %s:%d %s %s\n"
    slotAutoRebalance = "./bin/codis-config -c conf/config.ini slot rebalance\n"
    MasterPortList = [6000,6001,6002,6003,6004,6005]
    shellFileName = "tmp/" + codisName + ".sh"
    groupNo = newGid
    with open(shellFileName,'w') as f:
        for indexMaster,masterHost in enumerate(yzHostList):
            #if indexMaster = len(yzHostList)-1:
            if indexMaster == 1:
                slaveHost = yzHostList[indexMaster-1]
            else:
                slaveHost = yzHostList[indexMaster+1]

            for MasterPort in MasterPortList:
                f.write(codisServerAdd %(groupNo, masterHost, MasterPort, "master", "yz"))
                f.write(codisServerAdd %(groupNo, slaveHost, MasterPort+1000, "slave", "yz")) 
                f.write("sleep 1\n")
                groupNo += 1

        f.write("sleep 5\n")
        f.write(slotAutoRebalance)
    print "Create ConfigShell file Ok!"



codisName = sys.argv[1]
yzHosts = sys.argv[2]

if not codisName.endswith("-cache"):
	codisName += "-cache"

yzHostList = yzHosts.split(",")
for index, yzHost in enumerate(yzHostList):
    yzHostList[index] = yzHost.strip()

ApiIP = getApiIP(codisName)
print "Dashboard IP:", ApiIP

groupsInfo = getInfo(ApiIP)
#pprint(groupsInfo)

maxGid = getMaxGID(groupsInfo)
#print maxGid
newGid = maxGid + 1
print "New GID is:", newGid

configShell(codisName,yzHostList,newGid)


