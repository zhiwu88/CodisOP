#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import sqlite3

def getIPtoFile(codisName):
    Listfile = "/home/work/Ansible/" + codisName + "_hostlist"
    with open(Listfile, 'w') as f:
        f.write("[xy]\n")
        conn = sqlite3.connect('/home/work/CodisInstaller/tools/ClusterManager/ClusterManager.db')
        cursor = conn.execute('select ip from hostinfo where hostname like ?' , ('cds-' + codisName + '%.xy',))
        for row in cursor:
            f.write(row[0] + "\n")

        f.write("[yz]\n")
        conn = sqlite3.connect('/home/work/CodisInstaller/tools/ClusterManager/ClusterManager.db')
        cursor = conn.execute('select ip from hostinfo where hostname like ?' , ('cds-' + codisName + '%.yz',))
        for row in cursor:
            f.write(row[0] + "\n")

conn = sqlite3.connect('/home/work/CodisInstaller/tools/ClusterManager/ClusterManager.db')
cursor = conn.execute('select hostname from hostinfo where hostname not like ? and hostname not like ? and hostname not like ? and hostname not like ?' , ('cds-yc%','cds-zk%','cds-borui%','cds-op%'))
codisNameset = set()
for row in cursor:
    #print row[0].split('-')[1]
    codisNameset.add(row[0].split('-')[1])
for codisName in codisNameset:
    getIPtoFile(codisName)


