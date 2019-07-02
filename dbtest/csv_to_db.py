# encoding:utf-8

import os
import sys
import ConfigParser

sys.path.append("..\source_py")
from check_db import db_operate

reload(sys)
sys.setdefaultencoding("utf-8")


def main():
    if len(sys.argv) != 2:
        print "use: python csv_to_db csv_dir"
        exit(-1)
    csv_dir = sys.argv[1]
    print csv_dir
    cfg = ConfigParser.ConfigParser()
    cfg.read("utest.ini")
    db_user = cfg.get('db', 'user')
    db_password = cfg.get('db', 'password')
    db_host = cfg.get('db', 'host')
    db_port = cfg.get('db', 'port')
    db_database = cfg.get('db', 'curr_db')
    conn = db_operate.connect_db(db_user, db_password, db_host, db_port, db_database)
    admin_db = cfg.get("db", "admin_db")
    history_db = cfg.get("db", "history_db")
    init_db = cfg.get("db", "init_db")
    sync_db = cfg.get("db", "sync_db")

    db_operate.load_csv_into_db(conn, csv_dir, admin_db, history_db, init_db, sync_db)


if __name__ == '__main__':
    main()
