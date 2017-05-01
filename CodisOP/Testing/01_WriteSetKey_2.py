#!/usr/bin/env python

import redis
import string
import random
import time

r = redis.Redis(host='100.0.0.3', port=7000)

#letter26 = []
#for letter in string.lowercase:
#    letter26.append(letter)

n = 1
t1 = time.time()
while n <= 1000000:
    #rand_num = random.randrange(100,999,1)
    #rand_letter = string.join(random.sample(letter26,3)).replace(" ","")
    rand_str = "kkkkkkk"
    list_value = 'string_string_string_string_string_'

    r.setex(rand_str, list_value, 600)
    n += 1

t2 = time.time()
print("done: %f s" % (t2 - t1))
