#!/usr/bin/env python

import redis
import string
import random
from multiprocessing import Pool
import os
import traceback


def writeSetKey(num):
    proc = os.getpid()
    print "NO.", num, "process:" ,proc

    r = redis.Redis(host='100.0.0.3', port=6379, socket_timeout=5)
    
    n = 0
    #list_value = 'str'*29
    keystring = str(num).zfill(3)
    while n < 10000:
        #print n
        #rand_num = random.randrange(100,999,1)
        rand_letter = string.join(random.sample(string.lowercase,10)).replace(" ","")
        #rand_str = str(rand_letter) + str(rand_num) + str(n)
        rand_str = rand_letter + keystring + str(n).zfill(5)
        #str_value = ''.join(random.sample(string.letters,36))
        str_value = ''.join(random.sample(string.printable,87))
        try:
            r.set(rand_str, str_value, ex=3600)
        except:
            ferr = open("errorlog.txt",'a')
            traceback.print_exc(file=ferr)
            f.flush()
            f.close()
    
        n += 1
    print "Done" , proc


if __name__ == '__main__':

    p = Pool(processes=1000)
    p.map_async(writeSetKey, range(0,10000))
    p.close()
    p.join()

