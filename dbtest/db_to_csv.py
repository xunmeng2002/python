# encoding: utf-8
import os
import sys
import csv
import ConfigParser
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("../source_py")
from check_db import db_operate


def write_csv_with_table_name(cursor, db_name, short_db_name, table_name, dest_path):
    header = db_operate.qry_header_from_table(cursor, db_name, table_name)
    data = db_operate.qry_all_data_from_table(cursor, db_name, table_name)
    dest_name = short_db_name + "." + table_name + ".csv"
    dest_file = os.path.join(dest_path, dest_name)
    print dest_file
    write = csv.writer(open(dest_file, mode="wb"))
    write.writerow(header)
    for row in data:
        write.writerow(row)


def write_csv_with_db_name(cursor, db_name, short_db_name, dest_path):
    table_names = db_operate.qry_table_names(cursor, db_name)
    for table_name in table_names:
        write_csv_with_table_name(cursor, db_name, short_db_name, table_name, dest_path)


def get_db_name(cfg):
    admin_db = cfg.get("db", "admin_db")
    history_db = cfg.get("db", "history_db")
    init_db = cfg.get("db", "init_db")
    sync_db = cfg.get("db", "sync_db")
    db_name_dict = {}
    for i in range(2, len(sys.argv)):
        if sys.argv[i] == "*":
            db_name_dict["admin"] = admin_db
            db_name_dict["history"] = history_db
            db_name_dict["init"] = init_db
            db_name_dict["sync"] = sync_db
        elif sys.argv[i] == "admin":
            db_name_dict["admin"] = admin_db
        elif sys.argv[i] == "history":
            db_name_dict["history"] = history_db
        elif sys.argv[i] == "init":
            db_name_dict["init"] = init_db
        elif sys.argv[i] == "sync":
            db_name_dict["sync"] = sync_db
    return db_name_dict


if __name__ == '__main__':
    if len(sys.argv) < 3 or not os.path.isdir(sys.argv[1]):
        print "useage: python db_to_csv.py dest_dir db_name=*"
        exit(-1)
    cfg = ConfigParser.ConfigParser()
    cfg.read("utest.ini")
    db_user = cfg.get('db', 'user')
    db_password = cfg.get('db', 'password')
    db_host = cfg.get('db', 'host')
    db_port = cfg.get('db', 'port')
    db_database = cfg.get('db', 'curr_db')
    conn = db_operate.connect_db(db_user, db_password, db_host, db_port, db_database)
    cursor = conn.cursor()

    dest_dir = sys.argv[1]
    db_name_dict = get_db_name(cfg)
    for short_db_name in db_name_dict:
        write_csv_with_db_name(cursor, db_name_dict[short_db_name], short_db_name, dest_dir)

