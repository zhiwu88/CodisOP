#!/usr/bin/env 
# -*- encoding:utf-8 -*-

import sqlite3
import sys

def IsIP(expression):
  for c in expression:
    if (c < '0' or c > '9') and c != '.':
      return False
  return True

def DBSelect(expression):
  conn = sqlite3.connect('/home/work/CodisCenter/rsynccml/ClusterManager.db')
  cursor = None
  if expression == 'all':
    cursor = conn.execute('select * from hostinfo order by hostname ASC')
  else:
    cursor = conn.execute('select * from hostinfo where hostname like "%' + expression + '%" or ip like "%' + expression +'%" order by hostname ASC')
  for row in cursor:
    ifMatch = True
    if IsIP(expression):
      if expression[0] != '.' and expression.split('.')[0] != row[2].split('.')[0]:
        ifMatch = False
      if expression[-1] != '.':
        if expression.split('.')[-1] != row[2].split('.')[len(expression.split('.'))-1] \
         and expression.split('.')[-1] != row[2].split('.')[-1]:
          ifMatch = False

    if ifMatch:
      tabnum = 4 - len(row[1])/8
      if len(row[1])==22 or len(row[1])==23:
        tabnum -= 1
      print '\033[1;32;40m',
      print row[1],
      for i in range(tabnum):
        print '\t',
      print '\033[1;31;40m',
      print row[2],
      print '\033[0m'
  conn.close()
  
def DBSelect2(expression, room):
  conn = sqlite3.connect('/home/work/CodisInstaller/tools/ClusterManager/ClusterManager.db')
  cursor = None
  if expression == 'all':
    cursor = conn.execute('select * from hostinfo where hostname like "%.' + room + '" order by hostname ASC')
  else:
    cursor = conn.execute('select * from hostinfo where hostname like "%' + expression + '%.' + room + '" or ip like "%' + expression +'%" order by hostname ASC')
  for row in cursor:
    ifMatch = True
    if IsIP(expression):
      if expression[0] != '.' and expression.split('.')[0] != row[2].split('.')[0]:
        ifMatch = False
      if expression[-1] != '.':
        if expression.split('.')[-1] != row[2].split('.')[len(expression.split('.'))-1] \
         and expression.split('.')[-1] != row[2].split('.')[-1]:
          ifMatch = False

    if ifMatch:
      tabnum = 4 - len(row[1])/8
      if len(row[1])==22 or len(row[1])==23:
        tabnum -= 1
      print '\033[1;32;40m',
      print row[1],
      for i in range(tabnum):
        print '\t',
      print '\033[1;31;40m',
      print row[2],
      print '\033[0m'
  conn.close()

def DBInsert(hostname, ip):
  insertSQL = 'insert into hostinfo(hostname, ip, used) values("%s", "%s", %d)'
  conn = sqlite3.connect('/home/work/CodisInstaller/tools/ClusterManager/ClusterManager.db')
  conn.execute(insertSQL%(hostname, ip, 1))
  conn.commit()
  conn.close()

def DBDelete(hostname, ip):
  deleteSQL = 'delete from hostinfo where hostname = "%s" and ip = "%s"'
  conn = sqlite3.connect('/home/work/CodisInstaller/tools/ClusterManager/ClusterManager.db')
  conn.execute(deleteSQL%(hostname, ip))
  conn.commit()
  conn.close() 

def Usage():
  print '''\nUsage:
    python ClusterManager.py  list  hostnameOrIP
    python ClusterManager.py  list  all
    python ClusterManager.py  add   hostname\tIP
    python ClusterManager.py  del   hostname\tIP\n\n'''
   

def main(argv):
  if len(argv) == 3 and argv[1] == 'list':
    DBSelect(argv[2])
  elif len(argv) == 4 and argv[1] == 'list':
    DBSelect2(argv[2], argv[3])
  elif len(argv) == 4 and argv[1] == 'add':
    DBInsert(argv[2], argv[3])
  elif len(argv) == 4 and argv[1] == 'del':
    DBDelete(argv[2], argv[3])
  else:
    Usage()

if __name__ == '__main__':
  main(sys.argv)
