# encoding: utf-8
import sys
sys.path.append("..\..\source_py")
from check_db import csv_parse
from check_db import db_operate
from common_utils import db_struct


def main():
    db_user = "test"
    db_password = "Test@1234"
    db_host = "192.168.6.125"
    db_port = "3306"
    admin_db = "test_admin"
    history_db = "test_history"
    init_db = "test_init"
    sync_db = "test_sync"
    expect_path = "./expect/"
    conn = csv_parse.db_operate.connect_db(db_user, db_password, db_host, db_port, admin_db)
    cursor = conn.cursor()
    db_operate.load_csv_into_db(cursor, expect_path, admin_db, history_db, init_db, sync_db)
    db_info = db_struct.DbInfo(admin_db, history_db, init_db, sync_db)
    csv_parse.parse_csvs(cursor, expect_path, db_info)
    print "db_operate.check_result = %s, msg:\n%s" % db_operate.check_all_result(cursor, db_info)


if __name__ == '__main__':
    main()

