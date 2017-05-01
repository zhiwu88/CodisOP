#!/usr/bin/env python

import redis
import string
import random
from multiprocessing import Pool
import os


def writeSetKey(num):
    proc = os.getpid()
    print "process:" ,proc

    r1 = redis.Redis(host='100.0.0.1', port=9100, socket_timeout=2)
    r2 = redis.Redis(host='100.0.0.2', port=9200, socket_timeout=2)
    
    n = 1
    while n <= 1000000:
        rand_num = random.randrange(100,999,1)
        rand_letter = string.join(random.sample(string.letters,3)).replace(" ","")
        rand_str = rand_letter + str(num) + str(rand_num) + str(n)
        rand_str1 = rand_letter + str(rand_num) + str(n).zfill(5) + str(1).zfill(2)
        rand_str2 = rand_letter + str(rand_num) + str(n).zfill(5) + str(2).zfill(2)
        list_value = 'string_string_string_string_string_' + str(n)

        try:
            r1.setex(rand_str1, list_value, 7200)
            r2.setex(rand_str2, list_value, 7200)
        except Exception,ex:
            print Exception,":",ex
        n += 1

if __name__ == '__main__':
    p = Pool(processes=100)
    nlist = [x for x in range(0,100)]
    p.map(writeSetKey, nlist)
    p.close()
    p.join()

