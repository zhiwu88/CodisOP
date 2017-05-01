#!/usr/bin/env python

import redis
import string
import random

r1 = redis.Redis(host='10.0.0.24', port=9100)
#r2 = redis.Redis(host='10.0.0.6', port=9200)

letter26 = []
for letter in string.lowercase:
    letter26.append(letter)

n = 1
while n <= 1000000:
    rand_num = random.randrange(100,999,1)
    rand_letter = string.join(random.sample(letter26,3)).replace(" ","")
    rand_str1 = rand_letter + str(rand_num) + str(n).zfill(7) + str(1).zfill(2)
    #rand_str2 = rand_letter + str(rand_num) + str(n).zfill(7) + str(2).zfill(2)
    list_value = 'string_string_string_string_string_' + str(n)

    r1.set(rand_str1, list_value, ex=3600)
    #r2.set(rand_str2, list_value, ex=3600)
    n += 1
