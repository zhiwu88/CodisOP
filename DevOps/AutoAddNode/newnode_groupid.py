import urllib2
import sys
import json
import sqlite3
from pprint import pprint

#python newnode_groupid.py t1

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
	print APIURL
	response = urllib2.urlopen(APIURL)
	page_str = response.read()
	json_list = json.loads(page_str)
	#print json_list
	return json_list
	
def getMaxGID(groupsInfo):
	listID = []
	for group in groupsInfo:
		print group["id"]
		listID.append(group["id"])
	print listID
	print "MAX GID is:", max(listID)
	return max(listID)


codisName = sys.argv[1]
if not codisName.endswith("-cache"):
	codisName += "-cache"

ApiIP = getApiIP(codisName)
print ApiIP

groupsInfo = getInfo(ApiIP)
pprint(groupsInfo)

maxGid = getMaxGID(groupsInfo)
print maxGid


