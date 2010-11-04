from sql_common import *
import MySQLdb  
import logging

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
        
    def create_e(self):
        cursor = self._conn.cursor()  
        cursor.execute(MYSQL_CREATE_CMD) 
        self._conn.commit()
        cursor.close()
        
    def select_e (self):
        cursor = self._conn.cursor()
        cursor.execute(SELECT_CMD)
        cursor.close()
        
    def insert_fact_e (self):
        mysql_logger.info(">>>insert_fact_e<<<")
        cursor = self._conn.cursor()

        check_p = (0,10000,100000,1000000,10000000)
        index_i = 0
        t_s = time.time()
        for i in range(1,len(check_p) - 3):
            t = check_p[i] - check_p[i-1]
            #cal time here
            mysql_logger.info("==>>@%.3fs taken for {%s}" % (time.time() - t_s,index_i))
            for  ii in xrange(t):
                index_i += 1
                #action here
                cursor.execute(INSERT_CMD % (
                                        4000000207231448050 + index_i,
                                        3000000000000000050 + index_i,
                                        40000004 + index_i,
                                        time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
                                        time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
                                        time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
                                        time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
                                        ))
                self._conn.commit()
                pass            
        mysql_logger.info("==>>@%.3fs taken for {%s}" % (time.time() - t_s,index_i))
        
    @ExeTime
    def insert_e(self,n = 1000000):
        cursor = self._conn.cursor()  
        for i in range(n):
            cursor.execute(INSERT_CMD % (
                                        4000000207231448050+i,
                                        3000000000000000050+i,
                                        40000004+i,
                                        time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
                                        time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
                                        time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
                                        time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
                                        ))
            self._conn.commit()
        cursor.close()
            
    def update_e(self):
        cursor = self._conn.cursor()  
        cursor.execute(UPDATE_CMD)
        self._conn.commit()
        cursor.close()

    def update_random_e(self):
        cursor = self._conn.cursor()  
        cursor.execute(UPDATE_RANDOM_CMD)
        self._conn.commit()
        cursor.close()
        
    def del_e(self):
        cursor = self._conn.cursor()  
        cursor.execute(PG_DEL_CMD)
        self._conn.commit()
        cursor.close()
    
    def del_random_e(self):
        cursor = self._conn.cursor()  
        for i in range(5000):            
            cursor.execute(DEL_RANDOM_CMD)
        self._conn.commit()
        cursor.close()

class MySQLTester:
    def __init__ (self):
        pass

    def select_t ():
        mysql_p = MySQL_P()
        mysql_p.select_e()
        
    def insert_t1 (self):
        mysql_p = MySQL_P()
        mysql_p.insert_e()

    def insert_t2 (self):
        mysql_p = MySQL_P()  
        mysql_p.insert_e(100000)

    def insert_t3 (self):
        mysql_p = MySQL_P()
        mysql_p.insert_e(10000)

    def update_random_t (self):
        mysql_p = MySQL_P()
        mysql_p.update_random_e()

    @ExeTime
    def thread_t (self):
        import threading
        l = []
        for i in range(100) :
            t = threading.Thread(target = self.insert_t3)
            t.start()
            l.append(t)
        for t in l :
            t.join()
            
    @ExeTime
    def thread_mix_t (self):
        import threading
        l = []
        for i in range(10) :
            a = threading.Thread(target = self.insert_t3)
            a.start()
            l.append(a)
            b = threading.Thread(target = self.update_random_t)
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
    #mysql_p.insert_e(100)
    #mysql_p.update_e()
    #mysql_p.update_random_e()
    mysql_logger.info("end")
