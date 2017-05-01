#!/usr/bin/env python

import redis
import string
import random
from multiprocessing import Pool
import os
import traceback


def writeListKey(num):
    proc = os.getpid()
    print "NO.", num, "process:" , proc, "--writeListKey--"

    r = redis.StrictRedis(host='100.0.0.3', port=7000, socket_timeout=5, socket_connect_timeout=5)
    
    n = 0
    #list_key_str = 'key_list_'
    while n < 500000:
        #print n
        #list_key1 = list_key_str + '01' + str(num).zfill(3) + str(n).zfill(5)
        #list_key2 = list_key_str + '02' + str(num).zfill(3) + str(n).zfill(5)
        #str_value = ''.join(random.sample(string.printable,50))
        list_key1 = 'key_list'
        str_value = 'list_value'
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
    print "NO.", num, "process:" , proc, "--writeHashKey--"

    r = redis.StrictRedis(host='100.0.0.3', port=7000, socket_timeout=5, socket_connect_timeout=5)

    n = 0
    #hash_key_str = 'key_hash_'
    #keystring = str(num).zfill(3)
    while n < 500000:
        #hash_key = hash_key_str + str(num).zfill(3) + str(n).zfill(5)
        #rand_letter = string.join(random.sample(string.lowercase,10)).replace(" ","")
        #hash_field = rand_letter + keystring + str(n).zfill(5)
        #str_value = ''.join(random.sample(string.printable,87))
        hash_key = 'key_hash'
        hash_field = 'key_field' + str(n)
        str_value = 'hash_vvvvvvvvvvvvvvvvvvvvvvvvvv'
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
    print "NO.", num, "process:" , proc, "--writeSortedSetKey--"

    r = redis.StrictRedis(host='100.0.0.3', port=7000, socket_timeout=5, socket_connect_timeout=5)

    n = 0
    #sset_key_str = 'key_sortedset_'
    while n < 500000:
        #sset_key1 = sset_key_str + '01' + str(num).zfill(3) + str(n).zfill(5)
        #sset_key2 = sset_key_str + '02' + str(num).zfill(3) + str(n).zfill(5)
        #member = ''.join(random.sample(string.letters,10))
        sset_key1 = 'key_sortedset'
        member = 'user' + str(n)
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
    print "NO.", num, "process:" , proc, "--writeSetKey--"

    r = redis.StrictRedis(host='100.0.0.3', port=7000, socket_timeout=5, socket_connect_timeout=5)

    n = 0
    #set_key_str = 'key_set_'
    while n < 500000:
        #set_key = set_key_str + str(num).zfill(3) + str(n).zfill(5)
        #member = ''.join(random.sample(string.letters,10))
        set_key = 'key_set'
        
        try:
            #r.sadd(set_key, member)
            r.sadd(set_key, n)
        except:
            ferr = open("errorlog.txt",'a')
            traceback.print_exc(file=ferr)
            f.flush()
            f.close()

        n += 1
    print "Done" , proc


def writeStringKey(num):
    proc = os.getpid()
    print "NO.", num, "process:" ,proc, "--writeStringKey--"

    r = redis.StrictRedis(host='100.0.0.3', port=7000, socket_timeout=5, socket_connect_timeout=5)

    n = 0
    #string_key_str = 'key_string_'
    while n < 500000:
        #string_key = string_key_str + str(num).zfill(3) + str(n).zfill(5)
        #str_val = ''.join(random.sample(string.letters,10))
        string_key = 'key_string'
        str_val = 'string_string_string_string_string'
        try:
            r.set(string_key, str_val)
        except:
            ferr = open("errorlog.txt",'a')
            traceback.print_exc(file=ferr)
            f.flush()
            f.close()

        n += 1
    print "Done" , proc


if __name__ == '__main__':

    p = Pool(processes=1)
    p.map(writeStringKey, range(0,1))
    p.map(writeListKey, range(0,1))
    p.map(writeHashKey, range(0,1))
    p.map(writeSetKey, range(0,1))
    p.map(writeSortedSetKey, range(0,1))
    
    p.close()
    p.join()

