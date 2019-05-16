# encoding: utf-8
import sys
sys.path.append("..\..\source_py")
from check_db import csv_parse
from check_db import db_operate


def main():
    db_user = "test"
    db_password = "Test@1234"
    db_host = "192.168.6.125"
    db_port = "3306"
    db_admin = "test_admin"
    db_history = "test_history"
    db_init = "test_init"
    expect_path = "./expect/"
    conn = csv_parse.db_operate.connect_db(db_user, db_password, db_host, db_port, db_admin)
    cursor = conn.cursor()
    db_operate.load_csv_into_db(cursor, expect_path, db_admin, db_history, db_init)
    admin_tables = {}
    history_tables = {}
    init_tables = {}
    csv_parse.parse_csvs(cursor, expect_path, admin_tables, history_tables, init_tables, db_admin, db_history, db_init)

    print "db_operate.check_result = %s, msg:\n%s" % db_operate.check_result(cursor, db_admin, admin_tables)


if __name__ == '__main__':
    main()

