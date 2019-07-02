import csv
from common_utils import common_utils


def get_insert_sql_str(db_name, table_name, file_path):
    f = open(file_path, "r")
    reader = csv.reader(f)
    insert_sql = ""
    row_count = 0
    for row in reader:
        if row_count == 0:
            insert_sql += "insert into " + db_name + "." + table_name + "(" + ",".join(row) + ") values "
        else:
            if row_count > 1:
                insert_sql += ", "
            insert_sql += "("
            column_count = 0

            for item in row:
                item = common_utils.try_gbk2utf8(item)
                if column_count > 0:
                    insert_sql += ', '
                if item != "":
                    insert_sql += '"' + item + '"'
                else:
                    insert_sql += 'NULL'
                column_count += 1
            insert_sql += ")"
        row_count += 1
    insert_sql += ";"
    f.close()
    if row_count <= 1:
        insert_sql = ""
    print insert_sql
    return insert_sql
