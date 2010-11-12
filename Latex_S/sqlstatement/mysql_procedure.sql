
======================================test 1===============================================================
DROP procedure if exists pr_test;

DELIMITER |
create procedure pr_test()
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

select v_begindate,v_enddate,date(adddate(now(),-10));

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
 WHERE r.fax_start_date >=v_begindate and r.fax_start_date<=v_enddate and userid<>'80000050';
 
 select v_circuit_succ_cnt, v_circuit_fail_cnt, v_circuit_time,
       v_qadrecord_succ_cnt, v_qadrecord_fail_cnt, v_qadrecord_time,
       v_corecord_succ_cnt, v_corecord_fail_cnt, v_task_time,
       v_adrecordpage_succ_cnt, v_adrecordpage_fail_cnt, v_adtask_time,
       v_send_fail_cnt;
 
 END
|
DELIMITER ;


======================================run in client======================================================

call pr_test();



=================================test 2==================================================================

DROP TABLE IF EXISTS `tbl_fax_records_date`;
CREATE TABLE `tbl_fax_records_date` (
  `fax_start_date` datetime NOT NULL,
  PRIMARY KEY (`fax_start_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `tbl_today_areacode_statistics`;
CREATE TABLE `tbl_today_areacode_statistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `statday` varchar(20) DEFAULT '',
  `stattime` datetime DEFAULT NULL,
  `areacode` varchar(5) DEFAULT '' COMMENT '区号',
  `sendcnt` int(11) DEFAULT '0' COMMENT '发送数',
  `succeeds` int(11) DEFAULT '0' COMMENT '成功数',
  `retries` int(11) DEFAULT '0' COMMENT '重试数（呼叫数=成功+重试+失败）',
  `connectioncnt` int(11) DEFAULT '0' COMMENT '接通数',
  `faileds` int(11) DEFAULT '0' COMMENT '失败数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=130046 DEFAULT CHARSET=utf8;

========

drop procedure if exists pr2_test;
DELIMITER |
create procedure pr2_test()
BEGIN

declare v_date varchar(20) default date(adddate(now(),-1));
declare v_begindate varchar(25) default '';
declare v_enddate varchar(25) default '';
declare v_record_date_cnt int default 0;

set v_begindate = concat(v_date,' 00:00:00');
set v_enddate = concat(v_date,' 23:59:59');

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
     SELECT adddate(date(now()), -1),
            adddate(now(), -1),
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
|
DELIMITER ;

======================================run in client======================================================

call pr_test();
