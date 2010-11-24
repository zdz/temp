import time
import random
import logging
import datetime

SQL_SERVER_HOST='10.10.10.132'
#SQL_SERVER_HOST='localhost'
PG_SQL_USERNAME='postgres'
PG_SQL_PASSWORD='postgres'
SQL_USERNAME='root'
SQL_PASSWORD='111111'
SQL_DB='test12'
SQL_TABLE_INDEX = '3'
SQL_TABLE='tbl_fax_records%s' % SQL_TABLE_INDEX
CREATE_INDEX_SQL_CMD = 'CREATE INDEX index_ids_t ON %s(fax_start_date,fax_type, error, npages, time_long, area, retries);'% SQL_TABLE
PG_CREATE_INDEX_SQL_CMD = 'CREATE INDEX index_ids_t%s ON %s(fax_start_date,fax_type, error, npages, time_long, area, retries);'% (SQL_TABLE_INDEX,SQL_TABLE)

class SQL_Logger:
    def __init__ (self):        
        # set up logging to file - see previous section for more details
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename='sql_test.log',
                            filemode='a')
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

et_logger = g_SQL_Logger.getLogger('sqltest.extime')
etfh = logging.FileHandler('sqltest_exet.log')
etfh.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
et_logger.addHandler(etfh)

def ExeTime(func):
    def _func(*args, **args2):
        global et_logger        
        t0 = time.time()
        et_logger.info("@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__))
        et_logger.info("@%s running..." % (func.__name__))
        ret = func(*args, **args2)
        et_logger.info("@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__))
        et_logger.info("==>> %s <<==" % (func.__doc__))
        et_logger.info("==>>@%.3fs taken for {%s}" % (time.time() - t0, func.__name__))
        return ret
    return _func


PG_CREATE_CMD="""
CREATE TABLE %s (
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
  PRIMARY KEY (faxid)
) ;""" % SQL_TABLE

MYSQL_CREATE_CMD="""
CREATE TABLE IF NOT EXISTS `%s` (
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
  PRIMARY KEY (`faxid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;""" % SQL_TABLE

"""

INSERT INTO tbl_fax_records (faxid , taskid , fax_serv_addr , userid , receiver_number , status , fee , time_long , npages , error , error_descr , read_count , fax_start_date , fax_end_date , create_date , jobid , actual_fee , sip_descr , submit_date , kill_date ,  ext_delay , priority , fax_type , ts_type , origin_error , retries , max_retries , fax_res , fax_dcs , send_rate , send_res , send_2D , send_ecm , retry_type ,  recipient , recipient_company , area , number_type , hold_times)VALUES('8000000207231448050', '800000020723144805', '', '80000002', '079733445566', 3, 0.000, 0, 1, 13, NULL, 0, '2010-7-23 14:47:00', NULL, '2010-7-23 14:48:41', NULL, 0.000, NULL, '2010-7-23 14:47:00', '2010-7-24 14:47:00', 3, 105, 1, 0, NULL, 0, 3, 0,  NULL, NULL, 0, 0, 0, 0, 0,'dfd', '0797', 0,0);
delete from tbl_fax_records where faxid = '8000000207231448050';
update tbl_fax_records set fax_serv_addr = 'xx' where faxid = '8000000207231448050';
%

(
4000000207231448050+i,
3000000000000000050+i,
40000004+i
time.strftime('%Y-%m-d %H:%M:%S',time.localtime()),
)
"""


INSERT_CMD = """INSERT INTO %s (
faxid , taskid , fax_serv_addr , userid , receiver_number , 
status , fee , time_long , npages , error , 
error_descr , read_count , fax_start_date , fax_end_date , create_date , 
jobid , actual_fee , sip_descr , submit_date , kill_date , 
ext_delay , priority , fax_type , ts_type , origin_error , 
retries , max_retries , fax_res , fax_dcs , send_rate , 
send_res , send_2D , send_ecm , retry_type , recipient , 
recipient_company , area , number_type , hold_times) VALUES(
'%s', '%s', '', '%s', '079733445566',
3, 0.000, %s, %s, %s, 
NULL, 0, '%s', NULL, '%s', 
NULL, 0.000, NULL, '%s','%s',
3, 105, %s, 0, NULL, 
0, 3, 0, NULL, NULL, 
0, 0, 0, 0, 0,
'dfd', '0797', 0,0);"""

INSERT_CMD_DATA = lambda index_i:( 
                    SQL_TABLE,
                    4100000207231448050 + index_i,
                    4100000000000000050 + index_i,
                    41000004 + index_i,
                    random.randrange(20),
                    random.randrange(6),
                    random.randrange(13),
                    (datetime.datetime.now() + datetime.timedelta(random.randrange(-40,40))).strftime('%Y-%m-%d %H:%M:%S'),
                    (datetime.datetime.now() + datetime.timedelta(random.randrange(-40,40) - 40)).strftime('%Y-%m-%d %H:%M:%S'),
                    time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
                    time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
                    random.randrange(4)+1,)

SELECT_CMD="""SELECT COUNT(*) FROM tbl_fax_records3;"""


UPDATE_CMD="""update tbl_fax_records3 set fax_serv_addr = 'localhost';"""

UPDATE_RANDOM_CMD="""update tbl_fax_records set fax_serv_addr = 'localhost' where faxid in (select faxid from tbl_fax_records order by random() limit 1);"""

DEL_CMD="""delete from test_t;"""

DEL_RANDOM_CMD="""delete from tbl_fax_records where faxid in 
                (select faxid from tbl_fax_records order by random() limit 1);"""

###mysql
MYSQL_RANDOM_SEL_CMD="""select * from tbl_fax_records order by rand() limit 20;"""

CREATE_INDEX_CMD="""create index index_ids on tbl_fax_records(faxid,taskid);"""
DELETE_INDEX_CMD="""drop index index_ids on tbl_fax_records;"""


ALTER_T_ADD_COLUMN_CMD="""alter table tbl_fax_records add x  smallint(4);"""
ALTER_T_CHANGE_COLUMN_CMD="""alter table tbl_fax_records change x y integer;"""
ALTER_T_DEL_COLUMN_CMD="""alter table tbl_fax_records drop y;"""

ALTER_CHANGE_TABLE_NAME_CMD="""alter table tbl_fax_records rename to tbl_fax_records1;"""


#CREATE TRIGGER
"""
DROP TABLE IF EXISTS tab1;
CREATE TABLE tab1(
    tab1_id varchar(50)
);

DROP TRIGGER IF EXISTS t_afterinsert_on_tbl_fax_records3;
DELIMITER |

CREATE TRIGGER t_afterinsert_on_tbl_fax_records3
AFTER INSERT ON tbl_fax_records3
FOR EACH ROW
BEGIN
     insert into tab1(tab1_id) values(new.faxid);
END
|
 
DELIMITER ;

DROP TRIGGER IF EXISTS t_afterdelete_on_tbl_fax_records3;
DELIMITER |

CREATE TRIGGER t_afterdelete_on_tbl_fax_records3
AFTER DELETE ON tbl_fax_records3
FOR EACH ROW
BEGIN
      delete from tab1 where tab1_id=old.faxid;
END
|
 
DELIMITER ;
"""



###pgsql
PGSQL_RANDOM_SEL_CMD="""select * from tbl_fax_records order by random() limit 20;"""

CREATE_INDEX_CMD="""create index index_ids on tbl_fax_records(faxid,taskid);"""
PGSQL_DELETE_INDEX_CMD="""drop index index_ids;"""

PGSQL_ALTER_T_ADD_COLUMN_CMD="""alter table tbl_fax_records add column x smallint;"""
PGSQL_ALTER_T_CHANGE_COLUMN_CMD="""alter table tbl_fax_records rename column x TO y;
                                   alter table tbl_fax_records alter column y TYPE smallint;"""
PGSQL_ALTER_T_DEL_COLUMN_CMD="""alter table tbl_fax_records drop column x RESTRICT;"""

PGSQL_ALTER_CHANGE_TABLE_NAME_CMD="""alter table tbl_fax_records rename to tbl_fax_records1;"""



#trigger
"""
DROP TRIGGER IF EXISTS t_afterinsert_on_tbl_fax_records3 
ON tbl_fax_records3 RESTRICT;

CREATE OR REPLACE FUNCTION after_insert_tbl_fax_records3_func() 
RETURNS trigger AS $BODY$
BEGIN
INSERT INTO tab1(tab1_id) VALUES(NEW.faxid);
RETURN NULL;
END;
$BODY$
LANGUAGE 'plpgsql';

CREATE TRIGGER t_afterinsert_on_tbl_fax_records3
AFTER INSERT ON tbl_fax_records3
FOR EACH ROW
EXECUTE PROCEDURE after_insert_tbl_fax_records3_func();

DROP TRIGGER IF EXISTS t_afterdelete_on_tbl_fax_records3 
ON tbl_fax_records3 RESTRICT;

CREATE OR REPLACE FUNCTION after_delete_tbl_fax_records3_func() 
RETURNS trigger AS $BODY$
BEGIN
DELETE FROM tab1 WHERE tab1_id=OLD.faxid;
RETURN NULL;
END;
$BODY$
LANGUAGE 'plpgsql';

CREATE TRIGGER t_afterdelete_on_tbl_fax_records3
AFTER DELETE ON tbl_fax_records3
FOR EACH ROW
EXECUTE PROCEDURE after_delete_tbl_fax_records3_func();
"""




MYSQL_CREATE_PR_TEST = """
DROP procedure if exists pr_test%s;

DELIMITER |
create procedure pr_test%s()
BEGIN
DECLARE v_circuit_succ_cnt INT DEFAULT 0;
DECLARE v_circuit_fail_cnt INT DEFAULT 0;
DECLARE v_circuit_time INT DEFAULT 0;
DECLARE v_qadrecord_succ_cnt INT DEFAULT 0;
DECLARE v_qadrecord_fail_cnt INT DEFAULT 0;
DECLARE v_qadrecord_time INT DEFAULT 0;
DECLARE v_corecord_succ_cnt INT DEFAULT 0;
DECLARE v_corecord_fail_cnt INT DEFAULT 0;
DECLARE v_task_time INT DEFAULT 0;
DECLARE v_adrecordpage_succ_cnt INT DEFAULT 0;
DECLARE v_adrecordpage_fail_cnt INT DEFAULT 0;
DECLARE v_adtask_time INT DEFAULT 0;
DECLARE v_send_fail_cnt INT DEFAULT 0;

declare v_date varchar(20) default date(adddate(now(),-10));

declare v_begindate varchar(25) default '';
declare v_enddate varchar(25) default '';
declare v_record_date_cnt int default 0;

set v_begindate = concat(v_date,' 00:00:00');
set v_enddate = concat(v_date,' 23:59:59');


SELECT SQL_NO_CACHE 
       sum(CASE WHEN fax_type = 4 AND error = 1 THEN npages ELSE 0 END),
       sum(CASE WHEN fax_type = 4 AND error != 1 THEN npages ELSE 0 END),
       sum(CASE WHEN fax_type = 4 THEN time_long ELSE 0 END),
       sum(CASE WHEN fax_type = 3 AND error = 1 THEN npages ELSE 0 END),
       sum(CASE WHEN fax_type = 3 AND error != 1 THEN npages ELSE 0 END),
       sum(CASE WHEN fax_type = 3 THEN time_long ELSE 0 END),
       sum(CASE WHEN fax_type = 2 AND error = 1 THEN npages ELSE 0 END),
       sum(CASE WHEN fax_type = 2 AND error != 1 THEN npages ELSE 0 END),
       sum(CASE WHEN fax_type = 2 THEN time_long ELSE 0 END),
       sum(CASE WHEN fax_type = 1 AND error = 1 THEN npages ELSE 0 END),
       sum(CASE WHEN fax_type = 1 AND error != 1 THEN npages ELSE 0 END),
       sum(CASE WHEN fax_type = 1 THEN time_long ELSE 0 END),
       sum(CASE WHEN error >=100 and error<300 THEN npages ELSE 0 END)
  INTO v_circuit_succ_cnt, v_circuit_fail_cnt, v_circuit_time,
       v_qadrecord_succ_cnt, v_qadrecord_fail_cnt, v_qadrecord_time,
       v_corecord_succ_cnt, v_corecord_fail_cnt, v_task_time,
       v_adrecordpage_succ_cnt, v_adrecordpage_fail_cnt, v_adtask_time,
       v_send_fail_cnt
  FROM %s r
 WHERE r.fax_start_date >=v_begindate and r.fax_start_date<=v_enddate and userid<>'80000050';
 
 select SQL_NO_CACHE v_circuit_succ_cnt, v_circuit_fail_cnt, v_circuit_time,
       v_qadrecord_succ_cnt, v_qadrecord_fail_cnt, v_qadrecord_time,
       v_corecord_succ_cnt, v_corecord_fail_cnt, v_task_time,
       v_adrecordpage_succ_cnt, v_adrecordpage_fail_cnt, v_adtask_time,
       v_send_fail_cnt;
 
 END
|
DELIMITER ;
""" % (SQL_TABLE_INDEX,SQL_TABLE_INDEX,SQL_TABLE)

MYSQL_CREATE_PR2_TEST = """
drop procedure if exists pr2_test%s;

DELIMITER |
create procedure pr2_test%s()
BEGIN

declare v_date varchar(20) default date(adddate(now(),-10));

declare v_begindate varchar(25) default '';
declare v_enddate varchar(25) default '';
declare v_record_date_cnt int default 0;

set v_begindate = concat(v_date,' 00:00:00');
set v_enddate = concat(v_date,' 23:59:59');

SELECT SQL_NO_CACHE count(0)
     INTO v_record_date_cnt
    FROM tbl_fax_records_date
 WHERE fax_start_date >= v_begindate AND fax_start_date <= v_enddate;

IF v_record_date_cnt <1 then
    TRUNCATE tbl_fax_records_date;
    INSERT INTO tbl_fax_records_date
        SELECT SQL_NO_CACHE DISTINCT fax_start_date
              FROM %s
           WHERE fax_start_date >= v_begindate AND fax_start_date <= v_enddate;
END IF;


delete from tbl_today_areacode_statistics where statday = v_date;

INSERT INTO tbl_today_areacode_statistics(statday,
                                          stattime,
                                          areacode,
                                          sendcnt,
                                          succeeds,
                                          retries,
                                          connectioncnt,
                                          faileds)
     SELECT SQL_NO_CACHE 
            adddate(date(now()), -1),
            adddate(now(), -1),
            area,
            count(CASE WHEN error = 1 OR (error >= 100 AND error < 300) THEN 0 ELSE NULL END),
            count(CASE WHEN error = 1 THEN 0 ELSE NULL END),
            sum(retries),
            count(CASE WHEN error = 1 OR (error >= 102 AND error <= 105) THEN 0 ELSE NULL END),
            count(CASE WHEN error >= 100 AND error < 300 THEN 0 ELSE NULL END)
       FROM %s r, tbl_fax_records_date d
      WHERE r.fax_start_date = d.fax_start_date
   GROUP BY area;


END;
|
DELIMITER ;
""" % (SQL_TABLE_INDEX,SQL_TABLE_INDEX,SQL_TABLE,SQL_TABLE)


PGSQL_CREATE_PR_TEST = """
DROP FUNCTION IF EXISTS pr_test%s();
CREATE OR REPLACE FUNCTION pr_test%s()
RETURNS SETOF RECORD AS
$BODY$

DECLARE v_circuit_succ_cnt INT DEFAULT 0;
DECLARE v_circuit_fail_cnt INT DEFAULT 0;
DECLARE v_circuit_time INT DEFAULT 0;
DECLARE v_qadrecord_succ_cnt INT DEFAULT 0;
DECLARE v_qadrecord_fail_cnt INT DEFAULT 0;
DECLARE v_qadrecord_time INT DEFAULT 0;
DECLARE v_corecord_succ_cnt INT DEFAULT 0;
DECLARE v_corecord_fail_cnt INT DEFAULT 0;
DECLARE v_task_time INT DEFAULT 0;
DECLARE v_adrecordpage_succ_cnt INT DEFAULT 0;
DECLARE v_adrecordpage_fail_cnt INT DEFAULT 0;
DECLARE v_adtask_time INT DEFAULT 0;
DECLARE v_send_fail_cnt INT DEFAULT 0;

declare v_date varchar(20) default date(now() - interval '10 day');

declare v_begindate varchar(25) default '';
declare v_enddate varchar(25) default '';
declare v_record_date_cnt int default 0;
declare vbts timestamp;
declare vbte timestamp;
declare r int;
BEGIN

v_begindate := v_date || ' 00:00:00';
v_enddate := v_date || ' 23:59:59';

vbts := to_timestamp(v_begindate, 'YYYY-MM-DD HH24:MI:SS');
vbte := to_timestamp(v_enddate, 'YYYY-MM-DD HH24:MI:SS');

PERFORM v_begindate,v_enddate,date(now() - interval '10 day');

SELECT sum(CASE WHEN fax_type = 4 AND error = 1 THEN npages ELSE 0 END),
       sum(CASE WHEN fax_type = 4 AND error != 1 THEN npages ELSE 0 END),
       sum(CASE WHEN fax_type = 4 THEN time_long ELSE 0 END),
       sum(CASE WHEN fax_type = 3 AND error = 1 THEN npages ELSE 0 END),
       sum(CASE WHEN fax_type = 3 AND error != 1 THEN npages ELSE 0 END),
       sum(CASE WHEN fax_type = 3 THEN time_long ELSE 0 END),
       sum(CASE WHEN fax_type = 2 AND error = 1 THEN npages ELSE 0 END),
       sum(CASE WHEN fax_type = 2 AND error != 1 THEN npages ELSE 0 END),
       sum(CASE WHEN fax_type = 2 THEN time_long ELSE 0 END),
       sum(CASE WHEN fax_type = 1 AND error = 1 THEN npages ELSE 0 END),
       sum(CASE WHEN fax_type = 1 AND error != 1 THEN npages ELSE 0 END),
       sum(CASE WHEN fax_type = 1 THEN time_long ELSE 0 END),
       sum(CASE WHEN error >=100 and error<300 THEN npages ELSE 0 END)
  INTO v_circuit_succ_cnt, v_circuit_fail_cnt, v_circuit_time,
       v_qadrecord_succ_cnt, v_qadrecord_fail_cnt, v_qadrecord_time,
       v_corecord_succ_cnt, v_corecord_fail_cnt, v_task_time,
       v_adrecordpage_succ_cnt, v_adrecordpage_fail_cnt, v_adtask_time,
       v_send_fail_cnt
  FROM %s r
 WHERE r.fax_start_date >=vbts and r.fax_start_date<=vbte and userid<>'80000050';
 
return query select v_circuit_succ_cnt as v_circuit_succ_cnt, 
			v_circuit_fail_cnt as v_circuit_fail_cnt, 
			v_circuit_time as v_circuit_time,
			v_qadrecord_succ_cnt as v_qadrecord_succ_cnt, 
			v_qadrecord_fail_cnt as v_qadrecord_fail_cnt, 
			v_qadrecord_time as v_qadrecord_time,
			v_corecord_succ_cnt as v_corecord_succ_cnt, 
			v_corecord_fail_cnt as v_corecord_fail_cnt, 
			v_task_time as v_task_time,
			v_adrecordpage_succ_cnt as v_adrecordpage_succ_cnt, 
			v_adrecordpage_fail_cnt as v_adrecordpage_fail_cnt, 
			v_adtask_time as v_adtask_time,
			v_send_fail_cnt as v_send_fail_cnt;

END;
$BODY$
LANGUAGE 'plpgsql' VOLATILE;
""" % (SQL_TABLE_INDEX,SQL_TABLE_INDEX,SQL_TABLE)

PGSQL_CREATE_PR2_TEST="""
DROP FUNCTION IF EXISTS pr2_test%s();
CREATE OR REPLACE FUNCTION pr2_test%s()
RETURNS void AS
$BODY$

declare v_date varchar(20) default date(now() - interval '10 day');

/*declare v_begindate varchar(25) default '';
declare v_enddate varchar(25) default '';*/
declare v_record_date_cnt int default 0;

declare v_begindate timestamp;
declare v_enddate timestamp;
declare vbts varchar(25) default '';
declare vbte varchar(25) default '';

BEGIN

vbts := v_date || ' 00:00:00';
vbte := v_date || ' 23:59:59';

v_begindate := to_timestamp(vbts, 'YYYY-MM-DD HH24:MI:SS');
v_enddate := to_timestamp(vbte, 'YYYY-MM-DD HH24:MI:SS');

SELECT count(0)
     INTO v_record_date_cnt
    FROM tbl_fax_records_date
 WHERE fax_start_date >= v_begindate AND fax_start_date <= v_enddate;

IF v_record_date_cnt <1 then
    TRUNCATE tbl_fax_records_date;
    INSERT INTO tbl_fax_records_date
        SELECT DISTINCT fax_start_date
              FROM %s
           WHERE fax_start_date >= v_begindate AND fax_start_date <= v_enddate;
END IF;

delete from tbl_today_areacode_statistics where statday = v_date;

INSERT INTO tbl_today_areacode_statistics(statday,
                                          stattime,
                                          areacode,
                                          sendcnt,
                                          succeeds,
                                          retries,
                                          connectioncnt,
                                          faileds)
     SELECT date(now() - interval '10 day'),
            date(now() - interval '10 day'),
            area,
            count(CASE WHEN error = 1 OR (error >= 100 AND error < 300) THEN 0 ELSE NULL END),
            count(CASE WHEN error = 1 THEN 0 ELSE NULL END),
            sum(retries),
            count(CASE WHEN error = 1 OR (error >= 102 AND error <= 105) THEN 0 ELSE NULL END),
            count(CASE WHEN error >= 100 AND error < 300 THEN 0 ELSE NULL END)
       FROM %s r, tbl_fax_records_date d
      WHERE r.fax_start_date = d.fax_start_date
   GROUP BY area;

END;
$BODY$
LANGUAGE 'plpgsql' VOLATILE;
""" % (SQL_TABLE_INDEX,SQL_TABLE_INDEX,SQL_TABLE,SQL_TABLE)