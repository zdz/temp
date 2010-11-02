import pg
from sql_common import *


class PGTester():
    def __init__(self):
        self._db = pg.connect(dbname = SQL_DB,
                              host = SQL_SERVER_HOST,
                              user = PG_SQL_USERNAME,
                              passwd = SQL_PASSWORD)

    @ExeTime
    def create_e(self):
        self._db.query(PG_CREATE_CMD)
        
    @ExeTime
    def insert_e(self,n = 1000000):
        for i in range(n):
            self._db.query(INSERT_CMD % i)
            
    @ExeTime
    def update_e(self):
        self._db.query(UPDATE_CMD)
        
    @ExeTime
    def del_e(self):
        self._db.query(DEL_CMD)
    
    @ExeTime
    def del_random(self):
        for i in range(5000):
            self._db.query(DEL_RANDOM_CMD)
    
if __name__ == "__main__":
    pgtest = PGTester()
    pgtest.create_e()
    pgtest.insert_e()
    pgtest.update_e()
    