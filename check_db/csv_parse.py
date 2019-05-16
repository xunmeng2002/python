# coding:utf-8
import os
from common_utils import common_utils
import db_operate


def cmp_pk_with_other_table(table, other_table):
    for key_name in table.primary_key_name_list:
        if table.__getattribute__(key_name) != other_table.__getattribute__(key_name):
            return False
    return True


def cmp_total_with_other_table(table, other_table):
    for field_name in table.field_name_list:
        if table.__getattribute__(field_name) != other_table.__getattribute__(field_name):
            return False
    return True


def cmp_pk_with_value_dict(table, value_dict):
    for key_name in table.primary_key_name_list:
        if table.__getattribute__(key_name) != value_dict[key_name]:
            return False
    return True


def cmp_total_with_value_dict(table, field_dict):
    for field_name in table.field_name_list:
        if table.__getattribute__(field_name) != field_dict[field_name]:
            msg = "Table[%s] field name[%s] does not match. table value[%s], db value[%s]." % (table.table_name, field_name, table.__getattribute__(field_name), field_dict[field_name])
            msg += "\ntable:" + table.get_field_dict().__str__()
            msg += "\ndb:" + field_dict.__str__()
            return False, msg
    return True, ""


def get_primary_key_value_dict(table):
    if len(table.primary_key_value_dict) == 0:
        for field_name in table.primary_key_name_list:
            table.primary_key_value_dict[field_name] = table.__getattribute__(field_name)
    return table.primary_key_value_dict


def get_field_dict(table):
    if len(table.field_dict) == 0:
        for field_name in table.field_name_list:
            table.field_dict[field_name] = table.__getattribute__(field_name)
    return table.field_dict


def parse_one_csv_file(file_path, table_name, tables, primary_key_name_list):
    tables[table_name] = []
    row = 0
    Table = type(table_name, (object,), {})
    for line in open(file_path, "r"):
        line = common_utils.try_gbk2utf8(line)
        line = common_utils.trim_return(line)
        fields = line.split(",")
        if row == 0:
            Table.table_name = table_name
            Table.header_line = line
            Table.primary_key_name_list = primary_key_name_list
            Table.field_name_list = fields
            Table.primary_key_value_dict = {}
            Table.field_dict = {}
            Table.cmp_total_with_value_dict = cmp_total_with_value_dict
            Table.cmp_pk_with_value_dict = cmp_pk_with_value_dict
            Table.__eq__ = cmp_pk_with_other_table
            Table.cmp_pk_with_other_table = cmp_pk_with_other_table
            Table.cmp_total_with_other_table = cmp_total_with_other_table

            Table.get_primary_key_value_dict = get_primary_key_value_dict
            Table.get_field_dict = get_field_dict
        else:
            table = Table()
            column = 0
            for field in fields:
                table.__setattr__(Table.field_name_list[column], field)
                column += 1
            tables[table_name].append(table)
        row += 1


def parse_csvs(cursor, path, admin_tables, history_tables, init_tables, admindb_name, historydb_name, initdb_name):
    for file_name in os.listdir(path):
        if not file_name.endswith(".csv"):
            continue
        if file_name.startswith("admin"):
            curr_tables = admin_tables
            db_name = admindb_name
        elif file_name.startswith("history"):
            curr_tables = history_tables
            db_name = historydb_name
        elif file_name.startswith("init"):
            curr_tables = init_tables
            db_name = initdb_name
        else:
            print "unsupported file name[%s]." % file_name
            continue
        file_path = os.path.join(path, file_name)
        table_name = file_name.split(".")[1]
        primary_key_list = db_operate.qry_table_primary_key_list(cursor, db_name, table_name)
        parse_one_csv_file(file_path, table_name, curr_tables, primary_key_list)

