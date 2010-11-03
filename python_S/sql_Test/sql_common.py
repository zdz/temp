import time
import logging

#SQL_SERVER_HOST='10.10.10.128'
SQL_SERVER_HOST='localhost'
PG_SQL_USERNAME='postgres'
SQL_USERNAME='root'
SQL_PASSWORD='123456'
SQL_DB='test'

def ExeTime(func):
    def _func(*args, **args2):
        t0 = time.time()
        print "@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__)
        print "@%s running..." % (func.__name__)
        ret = func(*args, **args2)
        print "@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__)
        print "==>> %s <<==" % (func.__doc__)
        print "==>>@%.3fs taken for {%s}" % (time.time() - t0, func.__name__)
        return ret
    return _func

class SQL_Logger:
    def __init__ (self):        
        # set up logging to file - see previous section for more details
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename='myapp.log',
                            filemode='w')
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)

    def getLogger (self,s):
        return logging.getLogger(s)
        
g_SQL_Logger = SQL_Logger()

PG_CREATE_CMD="""
CREATE TABLE tbl_fax_records (
  faxid varchar(50) NOT NULL DEFAULT '',
  taskid varchar(50) DEFAULT NULL,
  fax_serv_addr varchar(30) DEFAULT NULL,
  userid varchar(20) DEFAULT NULL,
  receiver_number varchar(30) DEFAULT NULL,
  status integer NOT NULL,
  fee decimal(10,3) DEFAULT NULL,
  time_long smallint DEFAULT NULL,
  npages smallint DEFAULT NULL,
  error int DEFAULT NULL,
  error_descr varchar(250) DEFAULT NULL,
  read_count smallint DEFAULT NULL,
  fax_start_date timestamp DEFAULT NULL,
  fax_end_date timestamp DEFAULT NULL,
  create_date timestamp DEFAULT NULL,
  jobid varchar(15) DEFAULT NULL,
  actual_fee decimal(10,3) DEFAULT NULL,
  sip_descr varchar(200) DEFAULT NULL,
  submit_date timestamp DEFAULT NULL,
  kill_date timestamp DEFAULT NULL,
  ext_delay integer NOT NULL DEFAULT '3',
  priority integer NOT NULL DEFAULT '1',
  fax_type integer NOT NULL,
  ts_type integer NOT NULL DEFAULT '0',
  origin_error int DEFAULT NULL,
  retries integer NOT NULL DEFAULT '0',
  max_retries integer NOT NULL DEFAULT '2',
  fax_res integer DEFAULT NULL,
  fax_dcs varchar(16) DEFAULT NULL,
  send_rate integer DEFAULT NULL,
  send_res integer DEFAULT NULL,
  send_2D integer DEFAULT NULL,
  send_ecm integer DEFAULT NULL,
  retry_type integer NOT NULL DEFAULT '0',
  recipient varchar(30) DEFAULT NULL,
  recipient_company varchar(100) DEFAULT NULL,
  area varchar(5) DEFAULT NULL,
  number_type integer DEFAULT NULL,
  hold_times int DEFAULT NULL,
  PRIMARY KEY (faxid,taskid,priority,create_date,fax_serv_addr,fax_start_date,kill_date,status,error,fax_type,userid,receiver_number)
) ;"""

SELECT_CMD="""SELECT COUNT(*) FROM test_t;"""


UPDATE_CMD="""update tbl_fax_records set fax_serv_addr = 'localhost';"""

UPDATE_RANDOM_CMD="""update tbl_fax_records set fax_serv_addr = 'localhost' where faxid in (select faxid from tbl_fax_records order by random() limit 1);"""

DEL_CMD="""delete from test_t;"""

DEL_RANDOM_CMD="""delete from tbl_fax_records where faxid in 
                (select faxid from tbl_fax_records order by random() limit 1);"""

MYSQL_CREATE_CMD="""
CREATE TABLE IF NOT EXISTS `tbl_fax_records` (
  `faxid` varchar(50) NOT NULL DEFAULT '',
  `taskid` varchar(50) DEFAULT NULL,
  `fax_serv_addr` varchar(30) DEFAULT NULL,
  `userid` varchar(20) DEFAULT NULL,
  `receiver_number` varchar(30) DEFAULT NULL,
  `status` tinyint(4) NOT NULL,
  `fee` decimal(10,3) DEFAULT NULL,
  `time_long` smallint(6) DEFAULT NULL,
  `npages` smallint(6) DEFAULT NULL,
  `error` int(11) DEFAULT NULL,
  `error_descr` varchar(250) DEFAULT NULL,
  `read_count` smallint(6) DEFAULT NULL,
  `fax_start_date` datetime DEFAULT NULL,
  `fax_end_date` datetime DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `jobid` varchar(15) DEFAULT NULL,
  `actual_fee` decimal(10,3) DEFAULT NULL,
  `sip_descr` varchar(200) DEFAULT NULL,
  `submit_date` datetime DEFAULT NULL,
  `kill_date` datetime DEFAULT NULL,
  `ext_delay` tinyint(4) NOT NULL DEFAULT '3',
  `priority` tinyint(4) NOT NULL DEFAULT '1',
  `fax_type` tinyint(4) NOT NULL,
  `ts_type` tinyint(4) NOT NULL DEFAULT '0',
  `origin_error` int(11) DEFAULT NULL,
  `retries` tinyint(4) NOT NULL DEFAULT '0',
  `max_retries` tinyint(4) NOT NULL DEFAULT '2',
  `fax_res` tinyint(4) DEFAULT NULL,
  `fax_dcs` varchar(16) DEFAULT NULL,
  `send_rate` tinyint(4) DEFAULT NULL,
  `send_res` tinyint(4) DEFAULT NULL,
  `send_2D` tinyint(4) DEFAULT NULL,
  `send_ecm` tinyint(4) DEFAULT NULL,
  `retry_type` tinyint(4) NOT NULL DEFAULT '0',
  `recipient` varchar(30) DEFAULT NULL,
  `recipient_company` varchar(100) DEFAULT NULL,
  `area` varchar(5) DEFAULT NULL,
  `number_type` tinyint(4) DEFAULT NULL,
  `hold_times` int(11) DEFAULT NULL,
  PRIMARY KEY (`faxid`),
  KEY `fax_record_taskid` (`taskid`),
  KEY `idx_priority` (`priority`),
  KEY `idx_create_date` (`create_date`),
  KEY `idx_addr` (`fax_serv_addr`),
  KEY `idx_start_date` (`fax_start_date`),
  KEY `idx_kill_date` (`kill_date`),
  KEY `idx_status` (`status`),
  KEY `idx_error` (`error`),
  KEY `idx_fax_type` (`fax_type`),
  KEY `idx_user` (`userid`),
  KEY `idx_number` (`receiver_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

"""INSERT INTO tbl_fax_records (
faxid , taskid , fax_serv_addr , userid , receiver_number , status , fee , time_long , 
npages , error , error_descr , read_count , fax_start_date , fax_end_date
 , create_date , jobid , actual_fee , sip_descr , submit_date , kill_date , 
 ext_delay , priority , fax_type , ts_type , origin_error , retries , max_retries , 
 fax_res , fax_dcs , send_rate , send_res , send_2D , send_ecm , retry_type , 
 recipient , recipient_company , area , number_type , hold_times)
VALUES
('8000000207231448050', 
'800000020723144805', 
'', 
'80000002', 
'079733445566', 
3, 0.000, 0, 1, 13, NULL, 0, 
'2010-7-23 14:47:00', NULL, 
'2010-7-23 14:48:41', NULL, 0.000, NULL, 
'2010-7-23 14:47:00', 
'2010-7-24 14:47:00', 3, 105, 1, 0, NULL, 0, 3, 0, 
 NULL, NULL, 
0, 0, 0, 0, 0,
'dfd', '0797', 0,0);

%

(
4000000207231448050+i,
3000000000000000050+i,
40000004+i
time.strftime('%Y-%m-d %H:%M:%S',time.localtime()),
)
"""

INSERT_CMD = """INSERT INTO tbl_fax_records (
faxid , taskid , fax_serv_addr , userid , receiver_number , 
status , fee , time_long , npages , error , 
error_descr , read_count , fax_start_date , fax_end_date , create_date , 
jobid , actual_fee , sip_descr , submit_date , kill_date , 
ext_delay , priority , fax_type , ts_type , origin_error , 
retries , max_retries , fax_res , fax_dcs , send_rate , 
send_res , send_2D , send_ecm , retry_type , recipient , 
recipient_company , area , number_type , hold_times) VALUES(

'%s', '%s', '', '%s', '079733445566',
3, 0.000, 0, 1, 13, 
NULL, 0, '%s', NULL, '%s', 
NULL, 0.000, NULL, '%s','%s',
3, 105, 1, 0, NULL, 
0, 3, 0, NULL, NULL, 
0, 0, 0, 0, 0,
'dfd', '0797', 0,0);"""

bklkj="""
%

(
4000000207231448050+i,
3000000000000000050+i,
40000004+i
time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
)"""

###mysql
MYSQL_RANDOM_SEL_CMD="""select * from tbl_fax_records order by rand() limit 20;"""

CREATE_INDEX_CMD="""create index index_ids on tbl_fax_records(faxid,taskid);"""
DELETE_INDEX_CMD="""drop index index_ids on tbl_fax_records;"""


ALTER_T_ADD_COLUMN_CMD="""alter table tbl_fax_records add x  smallint(4);"""
ALTER_T_CHANGE_COLUMN_CMD="""alter table tbl_fax_records change x y integer;"""
ALTER_T_DEL_COLUMN_CMD="""alter table tbl_fax_records drop y;"""

ALTER_CHANGE_TABLE_NAME_CMD="""alter table tbl_fax_records rename to tbl_fax_records1;"""

###pgsql
PGSQL_RANDOM_SEL_CMD="""select * from tbl_fax_records order by random() limit 20;"""

CREATE_INDEX_CMD="""create index index_ids on tbl_fax_records(faxid,taskid);"""
PGSQL_DELETE_INDEX_CMD="""drop index index_ids;"""

PGSQL_ALTER_T_ADD_COLUMN_CMD="""alter table tbl_fax_records add column x smallint;"""
PGSQL_ALTER_T_CHANGE_COLUMN_CMD="""alter table tbl_fax_records rename column x TO y;
                                   alter table tbl_fax_records alter column y TYPE smallint;"""
PGSQL_ALTER_T_DEL_COLUMN_CMD="""alter table tbl_fax_records drop column x RESTRICT;"""

PGSQL_ALTER_CHANGE_TABLE_NAME_CMD="""alter table tbl_fax_records rename to tbl_fax_records1;"""