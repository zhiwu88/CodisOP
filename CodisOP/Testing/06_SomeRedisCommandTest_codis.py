#!/usr/bin/env python

import redis
import string
import random
from multiprocessing import Pool
import os
import traceback


def writeListKey(num):
    proc = os.getpid()
    print "NO.", num, "process:" ,proc

    r = redis.StrictRedis(host='100.0.0.4', port=9100, socket_timeout=5, socket_connect_timeout=5)
    
    n = 0
    list_key_str = 'key_list_'
    while n < 10000:
        #print n
        list_key1 = list_key_str + '01' + str(num).zfill(3) + str(n).zfill(5)
        list_key2 = list_key_str + '02' + str(num).zfill(3) + str(n).zfill(5)
        str_value = ''.join(random.sample(string.printable,50))
        try:
            r.lpush(list_key1, str_value)
            #r.lpushx(list_key, str_value)
            #r.rpush(list_key2, str_value)
            #r.rpushx(list_key, str_value)
        except:
            ferr = open("errorlog.txt",'a')
            traceback.print_exc(file=ferr)
            f.flush()
            f.close()
    
        n += 1
    print "Done" , proc


def writeHashKey(num):
    proc = os.getpid()
    print "NO.", num, "process:" ,proc

    r = redis.StrictRedis(host='100.0.0.4', port=9100, socket_timeout=5, socket_connect_timeout=5)

    n = 0
    hash_key_str = 'key_hash_'
    keystring = str(num).zfill(3)
    while n < 10000:
        hash_key = hash_key_str + str(num).zfill(3) + str(n).zfill(5)
        rand_letter = string.join(random.sample(string.lowercase,10)).replace(" ","")
        hash_field = rand_letter + keystring + str(n).zfill(5)
        str_value = ''.join(random.sample(string.printable,87))
        try:
            r.hset(hash_key, hash_field, str_value)
        except:
            ferr = open("errorlog.txt",'a')
            traceback.print_exc(file=ferr)
            f.flush()
            f.close()

        n += 1
    print "Done" , proc


def writeSortedSetKey(num):
    proc = os.getpid()
    print "NO.", num, "process:" ,proc

    r = redis.StrictRedis(host='100.0.0.4', port=9100, socket_timeout=5, socket_connect_timeout=5)

    n = 0
    sset_key_str = 'key_sortedset_'
    while n < 10000:
        sset_key1 = sset_key_str + '01' + str(num).zfill(3) + str(n).zfill(5)
        sset_key2 = sset_key_str + '02' + str(num).zfill(3) + str(n).zfill(5)
        member = ''.join(random.sample(string.letters,10))
        try:
            r.zadd(sset_key1, n, member)
            #r.zincrby(sset_key2, member, amount=n)
        except:
            ferr = open("errorlog.txt",'a')
            traceback.print_exc(file=ferr)
            f.flush()
            f.close()

        n += 1
    print "Done" , proc


def writeSetKey(num):
    proc = os.getpid()
    print "NO.", num, "process:" ,proc

    r = redis.StrictRedis(host='100.0.0.4', port=9100, socket_timeout=5, socket_connect_timeout=5)

    n = 0
    set_key_str = 'key_set_'
    while n < 10000:
        set_key = set_key_str + str(num).zfill(3) + str(n).zfill(5)
        member = ''.join(random.sample(string.letters,10))
        try:
            r.sadd(set_key, member)
        except:
            ferr = open("errorlog.txt",'a')
            traceback.print_exc(file=ferr)
            f.flush()
            f.close()

        n += 1
    print "Done" , proc



if __name__ == '__main__':

    p = Pool(processes=100)
    p.map_async(writeListKey, range(0,100))
    #p.map_async(writeHashKey, range(0,100))
    #p.map_async(writeSortedSetKey, range(0,100))
    #p.map_async(writeSetKey, range(0,100))
    p.close()
    p.join()

