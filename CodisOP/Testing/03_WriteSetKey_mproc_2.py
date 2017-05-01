#!/usr/bin/env python

import redis
import string
import random
from multiprocessing import Pool
import os
import time


def writeSetKey(num):
    proc = os.getpid()
    print "process:" ,proc

    r = redis.Redis(host='100.0.0.3', port=7000, socket_timeout=5)
    
    #letter26 = []
    #for letter in string.lowercase:
    #    letter26.append(letter)
    
    n = 1
    while n <= 100000:
        #rand_num = random.randrange(100,999,1)
        #rand_letter = string.join(random.sample(string.letters,3)).replace(" ","")
        #rand_str = rand_letter + str(num) + str(rand_num) + str(n)
        rand_str = "kkkkkkkk"
        list_value = 'string_string_string_string_string_'
        try:
            r.setex(rand_str, list_value, 3600)
        except Exception,ex:
            print Exception,":",ex
        n += 1

if __name__ == '__main__':
    t1 = time.time()
    p = Pool(processes=200)
    nlist = [x for x in range(0,200)]
    p.map(writeSetKey, nlist)
    p.close()
    p.join()
    t2 = time.time()
    print("done: {0} s".format(t2-t1))
