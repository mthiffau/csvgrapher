#!/usr/bin/python

import os,time

f = open('datapipe', 'w')

start = time.time()
last = start
i = 0
j = 0

while True:

    try:
        
        now = time.time()
        if (now - last) > 1:
            if j == 0:
                f.write("names,time,foo,bar\n")
            if j == 10:
                f.write("names,time,bar,foo\n")

            f.write(("%.3f" % (now - start)) + ',' + str(i) + ',' + str(i + 2) + '\n')
            f.flush()

            i = (i + 1) % 10
            j = (j + 1) % 20
            last = now
    except KeyboardInterrupt:
        break
    except Exception as ex:
        print("Exception: " + str(ex))

f.close()
