# encoding:utf-8
import os
import ConfigParser
import datetime
import sys
import re
import webbrowser as web
import test_struct

sys.path.append("..\source_py")
from check_db import db_operate

reload(sys)
sys.setdefaultencoding("utf-8")
# 参数，全局使用
arg_names = ['help', 'filter', 'suite-filter', 'only-load-data']
args = {}


def get_suites(root_dir, admin_db, history_db, init_db, sync_db):
    test_suites = []
    for name in os.listdir(root_dir):
        if name == 'report':
            continue
        suite_dir = os.path.join(root_dir, name)
        if not os.path.isdir(suite_dir):
            continue
        if "suite-filter" in args and re.search(args["suite-filter"], name) is None:
            continue
        suite = test_struct.TestSuite(name, suite_dir, get_cases(suite_dir, admin_db, history_db, init_db, sync_db))
        if len(suite.cases) > 0:
            test_suites.append(suite)
    return test_suites


def get_cases(suite_dir, admin_db, history_db, init_db, sync_db):
    cases = []
    for name in os.listdir(suite_dir):
        case_dir = os.path.join(suite_dir, name)
        if not os.path.isdir(case_dir):
            continue
        if "filter" in args and re.search(args["filter"], name) is None:
                continue
        cases.append(test_struct.TestCase(name, case_dir, admin_db, history_db, init_db, sync_db))
    return cases


def print_summary(suites):
    print 'test result:'
    for suite in suites:
        for case in suite.cases:
            if case.result:
                print 'pass  :[%s].%s' % (suite.name, case.name)
            else:
                print '  fail:[%s].%s' % (suite.name, case.name)


def parse_args():
    for i in range(1, len(sys.argv)):
        kv = sys.argv[i].split("=")
        if not kv[0].startswith('--') or kv[0][2:] not in arg_names:
            print 'error:%s is invalid argument' % kv[0]
            exit(-1)
        if len(kv) < 2:
            args[kv[0][2:]] = None
        else:
            args[kv[0][2:]] = kv[1]


def report(suites, start_time, end_time):
    html_name = os.path.join("./report", "report%s.html" % start_time.strftime("%Y%m%d_%H%M%S"))
    html = open(html_name, "wb")

    html.write("<!DOCTYPE html>																\n")
    html.write("<html>                                                      				\n")
    html.write("                                                            				\n")
    html.write("<head>                                                      				\n")
    html.write("	<meta charset=\"utf-8\">                                  				\n")
    html.write("	<title>测试结果</title>                                 				\n")
    html.write("	<style>                                                 				\n")
    html.write("		span{display:block;}                                				\n")
    html.write("		table {text-align: center;}                         				\n")
    html.write("		thead{ font-weight: bold;}                          				\n")
    html.write("		table, th, td {border: 1px solid gray;}             				\n")
    html.write("		th, td{padding: 7px 12px;white-space:pre-wrap;}                          				\n")
    html.write("		.pass { color: green;}                              				\n")
    html.write("		.error { color: red;}                               				\n")
    html.write("		.result_col { text-align: left;}                               		\n")
    html.write("	</style>                                                				\n")
    html.write("</head>                                                     				\n")

    html.write("<body style=\"padding: 30px 80px;\"> 										\n")
    html.write("	<span>开始时间:%s</span>\n" % start_time.strftime("%Y-%m-%d %H:%M:%S"))
    html.write("	<span>结束时间:%s</span>\n" % end_time.strftime("%Y-%m-%d %H:%M:%S"))
    html.write("	<span>执行时间:%d 秒</span>\n" % (end_time - start_time).seconds)

    case_pass_num = 0
    case_fail_num = 0
    suite_pass_num = 0
    suite_fail_num = 0
    for suite in suites:
        case_pass_num += suite.pass_num
        case_fail_num += suite.fail_num
        if suite.fail_num > 0:
            suite_fail_num += 1
        else:
            suite_pass_num += 1

    html.write("	<span>总共执行测试套件数量：%d，通过数量：%d，失败数量：%d</span>\n" % (
        suite_pass_num + suite_fail_num, suite_pass_num, suite_fail_num))
    html.write("	<span>总共执行测试用例数量：%d，通过数量：%d，失败数量：%d</span>\n" % (
        case_pass_num + case_fail_num, case_pass_num, case_fail_num))

    html.write("	<table style=\"margin-top: 30px;\">	                           				\n")
    html.write("		<thead>																	\n")
    html.write("			<tr>                                                                \n")
    html.write("				<th>测试套件</th>                                               \n")
    html.write("				<th>测试用例</th>                                               \n")
    html.write("				<th>结果</th>                                                   \n")
    html.write("				<th style=\"width:90px;\">耗时</th>                                                   \n")
    html.write("			</tr>                                                               \n")
    html.write("		</thead>                                                                \n")
    html.write("		<tbody>                                                                 \n")
    for suite in suites:
        first = True
        for case in suite.cases:
            html.write("			<tr>\n")
            if first:
                first = False
                html.write("				<td rowspan=\"%d\">%s(%d,%d)</td>\n" %
                           (len(suite.cases), suite.name, suite.pass_num + suite.fail_num, suite.fail_num))
            html.write("				<td>%s</td>\n" % case.name)
            if case.result:
                html.write("				<td class=\"result_col pass\">pass</td>\n")
            else:
                html.write("				<td class=\"result_col error\">failed:\n%s</td>\n" % case.msg)

            html.write("				<td >%d秒</td>\n" % case.elapse)
            html.write("			</tr>\n")

    html.write("		</tbody>                                                                \n")
    html.write("	</table>                                                                	\n")
    html.write("	</body>                                                                		\n")
    html.write("	</html>                                                                		\n")

    html.close()
    web.open_new_tab(html_name)


def show_help():
    print 'args:'
    print '  --filter=xxxxx       [optional] filt test case'
    print '  --suite-filter=xxxxx [optional] filt test suite'
    print '  --only-load-data     [optional] only load init data'
    print '  --help               [optional] show help info'


def main():
    parse_args()
    if 'help' in args:
        show_help()
        exit(0)
    cfg = ConfigParser.ConfigParser()
    cfg.read("utest.ini")
    db_user = cfg.get('db', 'user')
    db_password = cfg.get('db', 'password')
    db_host = cfg.get('db', 'host')
    db_port = cfg.get('db', 'port')
    db_database = cfg.get('db', 'curr_db')
    conn = db_operate.connect_db(db_user, db_password, db_host, db_port, db_database)
    cursor = conn.cursor()
    admin_db = cfg.get("db", "admin_db")
    history_db = cfg.get("db", "history_db")
    init_db = cfg.get("db", "init_db")
    sync_db = cfg.get("db", "sync_db")

    start_time = datetime.datetime.now()
    root_dir = cfg.get('path', 'root_dir')
    suites = get_suites(root_dir, admin_db, history_db, init_db, sync_db)
    for suite in suites:
        suite.exec_suite(cursor)
    end_time = datetime.datetime.now()
    report(suites, start_time, end_time)
    print_summary(suites)


if __name__ == '__main__':
    main()

