import pg
from sql_common import *
import logging
import time
import threading

pgsql_logger = g_SQL_Logger.getLogger('sqltest.postgresql')
fh = logging.FileHandler('postgresql_test.log')
fh.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
pgsql_logger.addHandler(fh)

class PGSQL_P:
    def __init__(self):
        self._db = pg.connect(dbname = SQL_DB,
                              host = SQL_SERVER_HOST,
                              user = PG_SQL_USERNAME,
                              passwd = PG_SQL_PASSWORD)

    def __del__ (self):
        self._db.close()
        
    @ExeTime
    def create_e(self):
        self._db.query(PG_CREATE_CMD)
    def exe_e (self,sql_cmd):
        self._db.query(sql_cmd)

    def select_e (self):
        self._db.query(SELECT_CMD)

    def update_e (self):
        self._db.query(UPDATE_CMD)

    def insert_fact_e (self):
        pgsql_logger.info(">>>insert_fact_e<<<")

        check_p = (0,10000,100000,1000000,10000000)
        index_i = 0
        t_s = time.time()
        for i in range(1,len(check_p)- SQL_TABLE_INDEX):
            t = check_p[i] - check_p[i-1]
            #cal time here
            pgsql_logger.info("==>>@%.3fs taken for {%s}" % (time.time() - t_s,index_i))
            for  ii in xrange(t):
                index_i += 1
                #action here
                self._db.query(INSERT_CMD % INSERT_CMD_DATA(index_i))

        pgsql_logger.info("==>>@%.3fs taken for {%s}" % (time.time() - t_s,index_i))
        
    @ExeTime
    def insert_e(self,n = 1000000,offset_ = 0):
        """ >>>PGTester.insert_e<<< """
        for i in range(n):
            self._db.query(INSERT_CMD % INSERT_CMD_DATA(i + offset_))
            

class PGTester:
    def __init__ (self):
        pass
        
    def select_t (self):
        pgsql_p = PGSQL_P()
        pgsql_p.select_e()

    def update_t (self):
        pgsql_p = PGSQL_P()
        pgsql_p.update_e()
        
    def insert_t (self,n = 10000, offset_ = 0):
        pgsql_p = PGSQL_P()
        pgsql_p.insert_e(n,offset_)

    def update_t (self):
        pgsql_p = PGSQL_P()
        pgsql_p.update_e()

    @ExeTime
    def thread_t (self):     
        """MySQLTester.thread_t"""
        l = []
        for i in range(50) :
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
    pgsql_logger.info("begin")
    pgsql_p = PGSQL_P()
    #pgsql_p.create_e()
    #pgsql_p.exe_e(PG_CREATE_INDEX_SQL_CMD)
    pgsql_p.exe_e(PGSQL_CREATE_PR_TEST)
    pgsql_p.exe_e(PGSQL_CREATE_PR2_TEST)
    #pgsql_p.insert_fact_e()
    #pgsql_p.insert_e(1000)   
    #pgtester=PGTester()
    #pgtester.thread_t()
    pgsql_logger.info("end")
    