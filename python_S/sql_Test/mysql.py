from sql_common import *
import MySQLdb  
import logging
import threading
mysql_logger = g_SQL_Logger.getLogger('sqltest.mysql')
fh = logging.FileHandler('mysql_test.log')
fh.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
mysql_logger.addHandler(fh)

class MySQL_P:
    def __init__(self):
        self._conn = MySQLdb.connect(host=SQL_SERVER_HOST, 
                                     user=SQL_USERNAME, 
                                     passwd=SQL_PASSWORD,
                                     db=SQL_DB)
        
    def __del__ (self):
        self._conn.close()
        
    def exe_e (self,sql_cmd):
        cursor = self._conn.cursor()  
        cursor.execute(sql_cmd) 
        self._conn.commit()
        cursor.close()
        
    def create_e(self):
        self.exe_e(MYSQL_CREATE_CMD)
        
    def select_e (self):
        self.exe_e(SELECT_CMD)
    
    def update_e (self):
        self.exe_e(UPDATE_CMD)
        
        
    def insert_fact_e (self):
        mysql_logger.info(">>>insert_fact_e<<<")
        cursor = self._conn.cursor()

        check_p = (0,10000,100000,1000000,10000000)
        index_i = 0
        t_s = time.time()
        for i in range(1,len(check_p)):
            t = check_p[i] - check_p[i-1]
            #cal time here
            mysql_logger.info("==>>@%.3fs taken for {%s}" % (time.time() - t_s,index_i))
            for  ii in xrange(t):
                index_i += 1
                #action here
                cursor.execute(INSERT_CMD % INSERT_CMD_DATA(index_i))
                self._conn.commit()
                pass            
        mysql_logger.info("==>>@%.3fs taken for {%s}" % (time.time() - t_s,index_i))
        
    @ExeTime
    def insert_e(self,n = 10000,offset_ = 0):
        """MySQL_P.insert_e"""
        cursor = self._conn.cursor()  
        for i in range(n):
            cursor.execute(INSERT_CMD % INSERT_CMD_DATA(i + offset_))
            self._conn.commit()
        cursor.close()
            
 

class MySQLTester:
    def __init__ (self):
        pass
        
    def select_t (self):
        mysql_p = MySQL_P()
        mysql_p.select_e()

    def update_t (self):
        mysql_p = MySQL_P()
        mysql_p.update_e()
        
    def insert_t (self,n = 10000, offset_ = 0):
        mysql_p = MySQL_P()
        mysql_p.insert_e(n,offset_)

    def update_random_t (self):
        mysql_p = MySQL_P()
        mysql_p.update_random_e()

    @ExeTime
    def thread_t (self):     
        """MySQLTester.thread_t"""
        l = []
        for i in range(100) :
            t = threading.Thread(target = self.insert_t,kwargs = {'offset_' :i*100000})
            t.start()
            l.append(t)
        for t in l :
            t.join()
            
    @ExeTime
    def thread_mix_t (self):
        l = []
        for i in range(10) :
            a = threading.Thread(target = self.insert_t,kwargs = {'offset_' :i*100000})
            a.start()
            l.append(a)
            b = threading.Thread(target = self.update_t)
            b.start()
            l.append(b)
            c = threading.Thread(target = self.select_t)
            c.start()
            l.append(c)
        for t in l :
            t.join()      
        


if __name__ == "__main__":
    mysql_logger.info("begin")
    mysql_p = MySQL_P()
    mysql_p.create_e()
    mysql_p.insert_fact_e()
    #mysql_p.insert_e(1000)
    #mysql_t = MySQLTester()
    #mysql_t.thread_t()
    mysql_logger.info("end")
