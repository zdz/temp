import threading
import time

class SQLTestThread(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name = threadname)
    def run(self):
        for i in range(10):
            print self.getName(), i
            

if __name__ == '__main__':
    l = []
    for i in range(10):        
        t = SQLTestThread('MyThread %s\n' % (i))
        t.start()
        l.append(t)
    for t in l:
        t.join()
        


    