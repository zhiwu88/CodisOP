#!/usr/bin/env python

import redis
import string
import random

r = redis.Redis(host='100.0.0.3', port=6379)

letter26 = []
for letter in string.lowercase:
    letter26.append(letter)

n = 1
while n <= 100000000:
    #rand_num = random.randrange(100,999,1)
    #rand_letter = string.join(random.sample(letter26,3)).replace(" ","")
    #rand_str = rand_letter + str(rand_num) + str(n)
    rand_str = string.join(random.sample(letter26,18)).replace(" ","")
    list_value = 'str'*12

    r.set(rand_str, list_value, ex=3600)
    n += 1
