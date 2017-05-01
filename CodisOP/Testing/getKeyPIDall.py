#!/bin/python

f = open("redis.log")
f.close
d = {}

for line in f.readlines():
        li = line.split()
        if len(li) != 10 and len(li) != 9:
                print line
                continue
        pid = int(li[0].split(":")[0])
        if d.has_key(li[-1]):
            d[li[-1]].append(pid)
        else:
            d[li[-1]] = []
            d[li[-1]].append(pid)

#with open("res.txt","w") as f:
#  #print d
#  for v in d.values():
#      if len(v) == 3:
#         #print "v"
#         f.write(str(v) + "\n")

with open("res_all.txt","w") as fa:
    for k,v in d.items():
        if len(v) == 3:
            fa.write(str(k) + ":" + str(v) + "\n")

