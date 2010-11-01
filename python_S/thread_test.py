import threading
import time

class MyThread(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name = threadname)
    def run(self):
        for i in range(10):
            print self.getName(), i
            time.sleep(1)

if __name__ == '__main__':
    t1 = MyThread('MyThread')
    print t1.getName(), t1.isDaemon() # False
    #t1.setDaemon(True)
    #print t1.getName(), t1.isDaemon() # True

    t1.start()
    print 'Main thread exit'
    print 'CurrentThread', threading.currentThread()
    print 'Enumrate', threading.enumerate()
    print 'ActiveCount', threading.activeCount()
    print 'IsAlive', t1.isAlive()
    t1.join()


    