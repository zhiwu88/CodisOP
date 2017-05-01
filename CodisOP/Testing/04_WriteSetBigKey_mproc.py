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
    
    #letter26 = []
    #for letter in string.lowercase:
    #    letter26.append(letter)

    n = 1
    list_value = 'string_'*5000
    keystring = "kkk" + str(num) + "kkk"
    while n <= 100:
        print n
        #rand_num = random.randrange(100,999,1)
        #rand_letter = string.join(random.sample(letter26,3)).replace(" ","")
        #rand_str = str(rand_letter) + str(rand_num) + str(n)
        rand_str = keystring + str(n)
        try:
            r.setex(rand_str, list_value, 3600)
        except:
            ferr = open("errorlog.txt",'a')
            traceback.print_exc(file=ferr)
            f.flush()
            f.close()
    
        n += 1
    print "Done" , proc


if __name__ == '__main__':

    #letter26 = []
    #for letter in string.lowercase:
    #    letter26.append(letter)

    p = Pool(processes=100)
    #nlist = [x for x in range(1,100)]
    #nlist = list(range(1,100))
    p.map_async(writeSetKey, range(0,100))
    p.close()
    p.join()

