#!/usr/bin/env python

import redis
import string
import random

r = redis.Redis(host='100.0.0.3', port=6379)

letter26 = []
for letter in string.lowercase:
    letter26.append(letter)

n = 1
while n <= 10000:
    rand_num = random.randrange(100,999,1)
    rand_letter = string.join(random.sample(letter26,3)).replace(" ","")
    rand_str = rand_letter + str(rand_num).zfill(3) + str(n).zfill(5)
    #list_value = 'string'
    #i = 0
    #while i <= 100000:
    #    list_value += 'string_string_string_string_string_'
    #    i += 1
    #print list_value
    list_value = 'string~' *5000
    r.setex(rand_str, list_value, 3600)
    n += 1
