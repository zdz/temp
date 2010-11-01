import time

def ExeTime(func):
    def _func(*args, **args2):
        t0 = time.time()
        print "@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__)
        print "@%s running..." % (func.__name__)
        ret = func(*args, **args2)
        print "@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__)
        print "==>>@%.3fs taken for {%s}" % (time.time() - t0, func.__name__)
        return ret
    return _func


PG_CREATE_CMD="""
CREATE TABLE  uchome_docomment (
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

INSERT_CMD="""INSERT INTO uchome_docomment (upid ,doid ,uid ,username ,dateline ,message ,ip ,grade)VALUES (
 '1', '2', '%s', 'myname', '1234567890', 'messagemessagemessagemessage', '127.0.0.1', '2'
)"""

UPDATE_CMD="update uchome_docomment set ip = 'localhost';"

DEL_CMD="delete from uchome_docomment;"

DEL_RANDOM_CMD="delete from uchome_docomment where uid in (select uid from uchome_docomment order by random() limit 1);"

(MyISAM_I,InnoDB_I)=range(2)
MYSQL_CREATE_CMD=("""
CREATE TABLE IF NOT EXISTS  uchome_docomment  (
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
CREATE TABLE IF NOT EXISTS  uchome_docomment  (
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
) ENGINE=InnoDB ;""")