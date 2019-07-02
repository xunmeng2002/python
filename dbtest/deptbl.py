# coding:utf-8
import sys
import re


class SP:
    def __init__(self):
        self.table_names = {}
        self.sp_names = {}
        self.name = ''


def get_sp_file_name(db_name):
    if db_name == 'history':
        return '../sql/historydb/create_historydb_sp.sql.tpl'
    elif db_name == 'admin':
        return '../sql/admindb/create_admindb_sp.sql.tpl'
    elif db_name == 'sync':
        return '../sql/syncdb/create_syncdb_sp.sql.tpl'
    elif db_name == 'init':
        return '../sql/initdb/create_initdb_sp.sql.tpl'
    else:
        return None


def parse_sp_file(file_name):
    sps = {}
    text = open(file_name, "rU").read()
    text = text.replace("create", "CREATE").replace("end ;;", "END ;;").replace("END;;", "END ;;")
    text = text.replace("`", "")
    text = text.replace('db, "', "db")
    text = text.replace('db,"', "db")
    end = 0
    begin = text.find('CREATE', end)
    while begin != -1:
        end = text.find("END ;;", begin)
        if end == -1:
            break
        sp = parse_sp(text[begin: end])
        sps[sp.name] = sp
        begin = text.find('CREATE', end)
    return sps


def parse_sp(sp_text):
    sp = SP()
    first = True
    tokens = re.split("[ (,)\r\n;]", sp_text)
    for token in tokens:
        if not token:
            continue
        if token.startswith("sp_") or token.startswith("func_"):
            if first:
                sp.name = token
                first = False
            else:
                sp.sp_names[token] = 1
        elif token.startswith("t_"):
            if token[2].islower():
                continue
            sp.table_names[token] = 1
        elif token.startswith("historydb.") or token.startswith("admindb."):
            sp.table_names[token] = 1
    return sp


def get_tables(sps, sp_name, walked_sps={}):
    tables = {}
    if sp_name not in sps.keys():
        print "%s not exist" % sp_name
        return tables

    sp = sps[sp_name]
    tables.update(sp.table_names)
    if sp.sp_names:
        for sub_sp_name in sp.sp_names:
            if sub_sp_name in walked_sps.keys():
                continue
            walked_sps[sub_sp_name] = 1
            tables.update(get_tables(sps, sub_sp_name, walked_sps))
    return tables


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "usage: python deptbl.py <history|admin|init|sync> <sp_name>"
        exit(0)
    print 'dbname=', sys.argv[1]
    print 'spname=', sys.argv[2]
    sp_file_name = get_sp_file_name(sys.argv[1])
    if sp_file_name is None:
        print "Invalid dbname"
        exit(-1)

    sps = parse_sp_file(sp_file_name)

    tables = get_tables(sps, sys.argv[2])
    if tables:
        for t in sorted(tables.keys(), key=str.lower):
            print t
    print "summary: %d tables" % len(tables.keys())
