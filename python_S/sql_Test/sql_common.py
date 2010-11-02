import time

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


PG_CREATE_CMD="""
CREATE TABLE  test_t (
  id serial,
  upid integer NOT NULL DEFAULT '0',
  doid integer  NOT NULL DEFAULT '0',
  uid integer  NOT NULL DEFAULT '0',
  username char(15) NOT NULL DEFAULT '',
  dateline integer NOT NULL DEFAULT '0',
  message text NOT NULL,
  ip char(20) NOT NULL DEFAULT '',
  grade integer NOT NULL DEFAULT '0',
  PRIMARY KEY (id,doid)
)  ;"""

SELECT_CMD="""SELECT COUNT(*) FROM test_t;"""

INSERT_CMD1="""INSERT INTO test_t (upid ,doid ,uid ,username ,dateline ,message ,ip ,grade)VALUES (
 '1', '2', '%s', 'myname', '1234567890', 'messagemessagemessagemessage', '127.0.0.1', '2'
)"""

UPDATE_CMD="""update test_t set ip = 'localhost';"""

UPDATE_RANDOM_CMD="""update test_t set ip = 'localhost' 
                     where uid in (select uid from test_t order by random() limit 1);"""

DEL_CMD="""delete from test_t;"""

DEL_RANDOM_CMD="""delete from test_t where uid in (select uid from test_t order by random() limit 1);"""

MYSQL_CREATE_CMD=("""
CREATE TABLE IF NOT EXISTS  test_t  (
   id  int(10) unsigned NOT NULL AUTO_INCREMENT,
   upid  int(10) unsigned NOT NULL DEFAULT '0',
   doid  mediumint(8) unsigned NOT NULL DEFAULT '0',
   uid  mediumint(8) unsigned NOT NULL DEFAULT '0',
   username  char(15) NOT NULL DEFAULT '',
   dateline  int(10) unsigned NOT NULL DEFAULT '0',
   message  text NOT NULL,
   ip  char(20) NOT NULL DEFAULT '',
   grade  smallint(6) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY ( id ),
  KEY  doid  ( doid )
) ENGINE=MyISAM ;"""
,"""
CREATE TABLE IF NOT EXISTS  test_t  (
   id  int(10) unsigned NOT NULL AUTO_INCREMENT,
   upid  int(10) unsigned NOT NULL DEFAULT '0',
   doid  mediumint(8) unsigned NOT NULL DEFAULT '0',
   uid  mediumint(8) unsigned NOT NULL DEFAULT '0',
   username  char(15) NOT NULL DEFAULT '',
   dateline  int(10) unsigned NOT NULL DEFAULT '0',
   message  text NOT NULL,
   ip  char(20) NOT NULL DEFAULT '',
   grade  smallint(6) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY ( id ),
  KEY  doid  ( doid )
) ENGINE=InnoDB ;"""
,
"""
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;""")

(MyISAM_I,InnoDB_I,InnoDB_I2)=range(len(MYSQL_CREATE_CMD))

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
NULL, 
'80000002', 
'079733445566', 
3, 0.000, 0, 1, 13, NULL, 0, 
'2010-7-23 14:47:00', NULL, 
'2010-7-23 14:48:41', NULL, 0.000, NULL, 
'2010-7-23 14:47:00', 
'2010-7-24 14:47:00', 3, 105, 1, 0, NULL, 0, 3, 0, 
NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 
'0797', 0,0);

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

'%s', '%s', NULL, '%s', '079733445566',
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