from common import *
import MySQLdb  



class MySQLTester():
    def __init__(self):
        self._conn = MySQLdb.connect(host='10.10.10.128', 
                                     user='root', 
                                     passwd='123456',
                                     db='test')
        

    @ExeTime
    def create_e(self,i = InnoDB_I):
        cursor = self._conn.cursor()  
        cursor.execute(MYSQL_CREATE_CMD[InnoDB_I]) 
        self._conn.commit()
        cursor.close()
        
    @ExeTime
    def insert_e(self):
        cursor = self._conn.cursor()  
        for i in range(10000):
            cursor.execute(INSERT_CMD % i)
        self._conn.commit()
        cursor.close()
            
    @ExeTime
    def update_e(self):
        cursor = self._conn.cursor()  
        cursor.execute(UPDATE_CMD)
        cursor.close()
        
    @ExeTime
    def del_e(self):
        cursor = self._conn.cursor()  
        cursor.execute(PG_DEL_CMD)
        cursor.close()
    
    @ExeTime
    def del_random(self):
        cursor = self._conn.cursor()  
        for i in range(5000):            
            cursor.execute(DEL_RANDOM_CMD)
        self._conn.commit()
        cursor.close()
            
if __name__ == "__main__":
    sqltester = MySQLTester()
    sqltester.create_e(InnoDB_I)
    sqltester.insert_e()
    sqltester.update_e()
