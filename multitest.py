import threading
import time

from datetime import datetime, timedelta

d = []


d = [i*100+50 for i in range (4)]
for row in d:
    if row % 250 == 0:
        print(row, "yes")
    else:
        print(row, "now")



#class ClockThread(threading.Thread):
#    def __init__(self,interval):
#        threading.Thread.__init__(self)
#        self.daemon = True
#        self.interval = interval
#    def run(self):
#        while True:
#            print("The time is %s" % time.ctime())
#            time.sleep(self.interval)
#t = ClockThread(15)
#t.start()

#def loop1(x):
#    for i in range(1,x):
#        print(i)

#def loop2(x):
#    for i in range(50,x):
#        print(i)


#e1 = threading.Event()
#e2 = threading.Event()

#t1 = threading.Thread(target = loop1, args=(10))
#t2 = threading.Thread(target = loop2, args=(60))

#t1.start()
#t2.start()

#e1.set()

#t1.join()
#t2.join()