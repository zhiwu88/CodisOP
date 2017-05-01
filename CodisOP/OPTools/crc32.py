#!/usr/bin/env python 

import binascii
import sys

key = sys.argv[1]

crc32value = binascii.crc32(key)

slotNo = crc32value % 1024

print "slotNo=" + str(slotNo)
