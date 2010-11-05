import pg
from sql_common import *
import logging
import time

pgsql_logger = g_SQL_Logger.getLogger('sqltest.postgresql')
fh = logging.FileHandler('postgresql_test.log')
fh.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
pgsql_logger.addHandler(fh)

class PGTester:
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

    def insert_fact_e (self):
        pgsql_logger.info(">>>insert_fact_e<<<")

        check_p = (0,10000,100000,1000000,10000000)
        index_i = 0
        t_s = time.time()
        for i in range(1,len(check_p)):
            t = check_p[i] - check_p[i-1]
            #cal time here
            pgsql_logger.info("==>>@%.3fs taken for {%s}" % (time.time() - t_s,index_i))
            for  ii in xrange(t):
                index_i += 1
                #action here
                self._db.query(INSERT_CMD % INSERT_CMD_DATA(index_i))

        pgsql_logger.info("==>>@%.3fs taken for {%s}" % (time.time() - t_s,index_i))
        
    @ExeTime
    def insert_e(self,n = 1000000):
        """ >>>PGTester.insert_e<<< """
        for i in range(n):
            self._db.query(INSERT_CMD % INSERT_CMD_DATA(i))
            
    
if __name__ == "__main__":
    pgsql_logger.info("begin")
    pgtest = PGTester()
    #pgtest.create_e()
    #pgtest.insert_fact_e()
    pgtest.insert_e(10000)    
    pgsql_logger.info("end")
    