#!/usr/bin/env python

import redis
import string
import random

r = redis.Redis(host='100.0.0.4', port=7000)

letter26 = []
for letter in string.lowercase:
    letter26.append(letter)

n = 1
while n <= 1000000:
    rand_num = random.randrange(100,999,1)
    rand_letter = string.join(random.sample(letter26,3)).replace(" ","")
    rand_str = rand_letter + str(rand_num) + str(n)
    list_value = 'string_string_string_string_string_' + str(n)

    r.setex(rand_str, list_value, 3600)
    n += 1
