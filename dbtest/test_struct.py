# encoding: utf-8
import os
import sys
import traceback
import datetime

sys.path.append("..\source_py")
from common_utils import common_utils
from common_utils import db_struct
from check_db import db_operate
from check_db import csv_parse


class TestSuite:
    def __init__(self, name, dir, cases):
        self.name = name
        self.cases = cases
        self.dir = dir
        self.fail_num = 0
        self.pass_num = 0

    def exec_suite(self, cursor):
        for case in self.cases:
            start = datetime.datetime.now()
            if case.exec_case(cursor):
                self.pass_num += 1
            else:
                self.fail_num += 1
            end = datetime.datetime.now()
            case.elapse = (end - start).seconds


class TestCase:
    def __init__(self, name, dir, admin_db, history_db, init_db, sync_db):
        self.name = name
        self.dir = dir
        self.admin_db = admin_db
        self.history_db = history_db
        self.init_db = init_db
        self.sync_db = sync_db
        self.command = ""
        self.result = True
        self.msg = ''
        self.elapse = 0
        self.read_command()

    def read_command(self):
        command_path = os.path.join(self.dir, "command.txt")
        for line in open(command_path):
            line = common_utils.trim_return(line)
            if line.find("#") > 0:
                line = line[:line.find("#")]
            self.command += line

    def replace_db_name(self, sql):
        sql = sql.replace('admin.', self.admin_db + '.')
        sql = sql.replace('history.', self.history_db + '.')
        sql = sql.replace('init.', self.init_db + '.')
        sql = sql.replace('sync.', self.sync_db + '.')
        sql = sql.replace('<admin>', self.admin_db)
        sql = sql.replace('<history>', self.history_db)
        sql = sql.replace('<init>', self.init_db)
        sql = sql.replace('<sync>', self.sync_db)
        return sql

    def check_expect(self, cursor, sql):
        if sql.startswith('EXPECT_NOT_EQUAL'):
            values = sql.replace('EXPECT_NOT_EQUAL', '').replace('(', '').replace(')', '').replace(';', '').split(',')
            return self.expect_not_equal(cursor, values[0], values[1])
        else:
            values = sql.replace('EXPECT', '').replace('(', '').replace(')', '').replace(';', '').split(',')
            return self.expect_equal(cursor, values[0], values[1])

    def expect_equal(self, cursor, value1, value2):
        sql1 = "select " + value1
        cursor.execute(sql1)
        v1 = cursor.fetchone()[0]
        sql2 = "select " + value2
        cursor.execute(sql2)
        v2 = cursor.fetchone()[0]
        if v1 != v2:
            self.result = False
            self.msg = "EXPECT(%s,%s):[%s]不等于[%s]" % (value1, value2, str(v1), str(v2))
            return False
        return True

    def expect_not_equal(self, cursor, value1, value2):
        sql1 = "select " + value1
        cursor.execute(sql1)
        v1 = cursor.fetchone()[0]
        sql2 = "select " + value2
        cursor.execute(sql2)
        v2 = cursor.fetchone()[0]
        if v1 == v2:
            self.result = False
            self.msg = "EXPECT_NOT_EQUAL(%s,%s):[%s]等于[%s]" % (value1, value2, str(v1), str(v2))
            return False
        return True

    def exec_case(self, cursor):
        try:
            init_dir = os.path.join(self.dir, "init")
            expect_dir = os.path.join(self.dir, "expect")
            db_operate.load_csv_into_db(cursor, init_dir, self.admin_db, self.history_db, self.init_db, self.sync_db)
            sqls = common_utils.trim_return(self.command).split(';')
            for sql in sqls:
                sql = self.replace_db_name(sql)
                if sql == '':
                    continue
                elif sql.startswith("EXPECT"):
                    if self.result is False:
                        return False
                else:
                    try:
                        cursor.execute(sql)
                    except Exception, e:
                        print sql
                        raise e
            db_info = db_struct.DbInfo(self.admin_db, self.history_db, self.init_db, self.sync_db)
            csv_parse.parse_csvs(cursor, expect_dir, db_info)
            self.result, self.msg = db_operate.check_all_result(cursor, db_info)
            return self.result
        except Exception, e:
            self.msg = traceback.format_exc()
            self.result = False
            return self.result
