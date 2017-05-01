#!/usr/bin/env python

import os
import sys
import commands

NotSupportCommandList=['keys *',
                    'migrate 127.0.0.1 6000 kk 20',
                    'move k 1',
                    'object refcount k',
                    'randomkey',
                    'rename k k2',
                    'renamenx k k2',
                    'scan 0',
                    'bitop k k2',
                    'msetnx k v',
                    'blpop klist 22',
                    'brpop k2 222',
                    'brpoplpush k2 k3 222',
                    #'psubscribe it*',
                    'publish msg "good"',
                    'punsubscribe it*',
                    #'subscribe msg charrim',
                    'unsubscribe ite*',
                    'discard ',
                    'watch k',
                    'multi',
                    'unwatch k',
                    'script load a',
                    'bgrewriteaof',
                    'bgsave',
                    'client kill',
                    'config set maxmemory 1024',
                    'dbsize',
                    'debug',
                    'flushall',
                    'flushdb',
                    'lastsave',
                    #'monitor',
                    'restore k',
                    'save',
                    'shutdown',
                    'slaveof 127.0.0.1 9200',
                    'slowlog get',
                    'sync',
                    'time',
                    'slotscheck',
                    'slotsdel 20',
                    'slotsinfo',
                    'slotsmgrtone 22',
                    'slotsmgrtslot 22',
                    'slotsmgrttagone',
                    'slotsmgrttagslot'
                    ]

if len(sys.argv) != 3:
  print '''Usage:
    python CodisProxyCommandTest.py ProxyIP PorxyPort'''
  exit()

for proxyCommand in NotSupportCommandList:
  command = "echo '" + proxyCommand +"'|./codis_6000/bin/redis-cli -h " + sys.argv[1] +" -p " + sys.argv[2]
  status, output = commands.getstatusoutput(command)
  print "command='" + proxyCommand + "'"
  print "ret='" + output + "'"
