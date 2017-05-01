#!/usr/bin/env python
import redis

conn = redis.StrictRedis(host='10.0.0.5', port='9100')

index = 1
with open("ScanMultiPrefixKey2f_test.txt", "r") as f:
    while True:
        line = f.readline()
        if line:
            key = line[0:-1]
            print index
            print key
            print conn.delete(key)
            index += 1
        else:
            break
