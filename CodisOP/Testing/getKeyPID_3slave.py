#!/bin/python

f = open("redis.log")
f.close
d = {}

for line in f.readlines():
        li = line.split()
        if len(li) != 10 and len(li) != 9:
                print line
                continue
        #pid = int(li[0].split(":")[0])
        pid = li[0]
        if d.has_key(li[-1]):
            d[li[-1]].append(pid)
        else:
            d[li[-1]] = []
            d[li[-1]].append(pid)

with open("res.txt","w") as f:
    #print d
    for k,v in d.items():
        if len(v) == 5:
            #print "v"
            f.write(str(v) + "\n")
        elif k != "ACK" and k != "GETACK" and k != "get":
            print str(k) + ":" + str(v)
        #else:
        #    print str(k) + ":" + str(v)

#with open("res_all.txt","w") as fa:
#    for k,v in d.items():
#        if len(v) == 3:
#            fa.write(str(k) + ":" + str(v) + "\n")

