#!/usr/bin/env python

import redis
import string
import random
from multiprocessing import Pool
import os
import traceback
import sys


def writeSetKey(num):
    proc = os.getpid()
    print "NO.", num, "process:" ,proc

    r = redis.Redis(host='100.0.0.3', port=6005, socket_timeout=5)
    
    #letter26 = []
    #for letter in string.lowercase:
    #    letter26.append(letter)

    n = 1
    list_value = 'string'
    list_value += 'string_string_string_string_string_'*100000
    while n <= 100:
        print n
        rand_num = random.randrange(100,999,1)
        rand_letter = string.join(random.sample(letter26,3)).replace(" ","")
        rand_str = str(rand_letter) + str(rand_num) + str(n)
        try:
            r.set(rand_str, list_value, ex=3600)
        except:
            print sys.exc_info()
    
        n += 1
    print "Done" , proc


if __name__ == '__main__':

    letter26 = []
    for letter in string.lowercase:
        letter26.append(letter)

    p = Pool(processes=10)
    #nlist = [x for x in range(1,100)]
    #nlist = list(range(1,100))
    p.map_async(writeSetKey, range(0,20))
    p.close()
    p.join()

