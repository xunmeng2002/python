# coding:utf-8
import os
import mysql.connector
from common_utils import common_utils


def connect_db(db_user, db_password, db_host, db_port, db_database):
    conn = mysql.connector.connect(user=db_user, password=db_password, host=db_host, port=db_port, database=db_database, charset='utf8')
    return conn


def load_csv_into_db(cursor, path, admin_db_name, history_db_name, init_db_name):
    for file_name in os.listdir(path):
        try:
            table_name = file_name.split('.')[1]
            db_name = ""
            if file_name.startswith("admin"):
                db_name = admin_db_name
            elif file_name.startswith("history"):
                db_name = history_db_name
            elif file_name.startswith("init"):
                db_name = init_db_name

            sql = "truncate " + db_name + "." + table_name + ";"
            cursor.execute(sql)
            file_path = path + file_name
            line_count = 0
            header_line = ''
            for line in open(file_path, "r"):
                line = common_utils.try_gbk2utf8(line)
                line = common_utils.trim_return(line)
                if line_count == 0:
                    header_line = line
                else:
                    values = line.split(",")
                    sql = "insert into " + db_name + "." + table_name + "(" + header_line + ") values("
                    i = 0
                    for value in values:
                        if i > 0:
                            sql += ', '
                        if value != '':
                            sql += '"' + value + '"'
                        else:
                            sql += 'NULL'
                        i += 1
                    sql += ");"
                    # print sql
                    cursor.execute(sql)
                line_count += 1
        except Exception, e:
            print "load %s failed" % file_name
            raise e


def check_result(cursor, db_name, all_tables):
    for table_name in all_tables:
        result, msg = check_one_table_records(cursor, db_name, table_name, all_tables[table_name])
        if not result:
            return False, msg
    return True, ""


def check_one_table_records(cursor, db_name, table_name, tables):
    sql = "select * from `" + db_name + "`.`" + table_name + "`;"
    cursor.execute(sql)
    res_list = cursor.fetchall()
    if len(res_list) != len(tables):
        return False, "db' records count doesn't match with Table[%s]." % table_name
    if len(tables) == 0:
        return True, ""

    first_table = tables[0]
    primary_key_list = first_table.primary_key_name_list
    field_name_list = first_table.field_name_list
    result, msg = check_one_table_records_primary_key_value(cursor, db_name, table_name, tables, primary_key_list)
    if not result:
        return False, msg
    result, msg = check_one_table_records_total_value(cursor, db_name, table_name, tables, field_name_list)
    if not result:
        return False, msg
    return True, msg


def check_one_table_records_primary_key_value(cursor, db_name, table_name, tables, primary_key_list):
    db_primary_key_value_dicts = qry_table_field_value_dicts(cursor, db_name, table_name, primary_key_list)
    for db_primary_key_value_dict in db_primary_key_value_dicts:
        is_exist = False
        for table in tables:
            if table.cmp_pk_with_value_dict(db_primary_key_value_dict):
                is_exist = True
                break
        if is_exist is False:
            msg = "Table[%s] record in db not exist in tables.\n" % table_name
            msg += db_primary_key_value_dict.__str__()
            return False, msg

    for table in tables:
        is_exist = False
        for db_primary_key_value_dict in db_primary_key_value_dicts:
            if table.cmp_pk_with_value_dict(db_primary_key_value_dict):
                is_exist = True
                break
        if is_exist is False:
            msg = "Table[%s] record in tables not exist in db.\n" % table_name
            msg += table.get_primary_key_value_dict()
            return False, msg

    return True, ""


def check_one_table_records_total_value(cursor, db_name, table_name, tables, field_name_list):
    db_field_value_dicts = qry_table_field_value_dicts(cursor, db_name, table_name, field_name_list)
    for db_field_value_dict in db_field_value_dicts:
        for table in tables:
            if table.cmp_pk_with_value_dict(db_field_value_dict):
                result, msg = table.cmp_total_with_value_dict(db_field_value_dict)
                if not result:
                    return False, msg
                break
    return True, ""


def qry_table_primary_key_list(cursor, db_name, table_name):
    sql = "SELECT t.COLUMN_NAME FROM `information_schema`.`KEY_COLUMN_USAGE` t where t.CONSTRAINT_NAME = 'PRIMARY' and t.TABLE_SCHEMA = '" + db_name + \
          "' and t.TABLE_NAME = '" + table_name + "' ORDER BY t.ORDINAL_POSITION;"
    cursor.execute(sql)
    primary_key_list = []
    for data in cursor.fetchall():
        primary_key_list.append(data[0].encode("utf-8"))
    return primary_key_list


def qry_table_field_value_dicts(cursor, db_name, table_name, field_name_list):
    sql = "select " + ", ".join(field_name_list) + " from `" + db_name + "`.`" + table_name + "`;"
    cursor.execute(sql)
    result_dicts = []
    for data in cursor.fetchall():
        count = 0
        result = {}
        for field_name in field_name_list:
            if data[count] is None:
                result[field_name] = ""
            elif type(data[count]).__name__ == "unicode":
                result[field_name] = data[count].encode("utf-8")
            elif type(data[count]).__name__ == "Decimal":
                result[field_name] = common_utils.transfer_decimal(data[count])
            else:
                result[field_name] = str(data[count])
            count += 1
        result_dicts.append(result)
    return result_dicts

