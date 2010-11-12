
======================================test 1===============================================================
DROP FUNCTION IF EXISTS pr_test();
CREATE OR REPLACE FUNCTION pr_test()
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
  FROM tbl_fax_records r
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



======================================run in client======================================================

SELECT * from pr_test() AS foo(v_circuit_succ_cnt INT, 
				v_circuit_fail_cnt INT, 
				v_circuit_time INT,
				v_qadrecord_succ_cnt INT, 
				v_qadrecord_fail_cnt INT, 
				v_qadrecord_time INT,	
				v_corecord_succ_cnt INT, 
				v_corecord_fail_cnt INT, 
				v_task_time INT,
				v_adrecordpage_succ_cnt INT, 
				v_adrecordpage_fail_cnt INT, 
				v_adtask_time INT,v_send_fail_cnt INT);


=================================test 2==================================================================

DROP TABLE IF EXISTS tbl_fax_records_date;
CREATE TABLE tbl_fax_records_date (
  fax_start_date timestamp NOT NULL,
  PRIMARY KEY (fax_start_date)
) ;

DROP TABLE IF EXISTS tbl_today_areacode_statistics;
DROP SEQUENCE IF EXISTS id_seq;
CREATE SEQUENCE id_seq;
CREATE TABLE tbl_today_areacode_statistics (
  id INTEGER DEFAULT NEXTVAL('id_seq'),
  statday varchar(20) DEFAULT '',
  stattime timestamp DEFAULT NULL,
  areacode varchar(5) DEFAULT '',
  sendcnt INTEGER DEFAULT '0',
  succeeds INTEGER DEFAULT '0',
  retries INTEGER DEFAULT '0',
  connectioncnt INTEGER DEFAULT '0',
  faileds INTEGER DEFAULT '0',
  PRIMARY KEY (id)
) ;

========
DROP FUNCTION IF EXISTS pr2_test();
CREATE OR REPLACE FUNCTION pr2_test()
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
              FROM tbl_fax_records
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
       FROM tbl_fax_records r, tbl_fax_records_date d
      WHERE r.fax_start_date = d.fax_start_date
   GROUP BY area;

END;
$BODY$
LANGUAGE 'plpgsql' VOLATILE;

======================================run in client======================================================

SELECT pr2_test();

