# encoding: utf-8

import os
import sys
import pandas as pd
import xlrd
reload(sys)
sys.setdefaultencoding("utf-8")


def get_excel_header(src_file):
    workbook = xlrd.open_workbook(src_file)
    table = workbook.sheet_by_index(0)
    row_value = [i for i in table.row_values(0)]
    return row_value


def xlsx_to_csv(src_file, dest_file):
    data_xlsx = pd.read_excel(src_file, dtype=str)
    data_xlsx.to_csv(dest_file, index=False, encoding="utf-8")


def xlsx_to_csv_with_dir(target_dir):
    for file_name in os.listdir(target_dir):
        if not file_name.endswith('.xlsx'):
            continue
        src_file = os.path.join(target_dir, file_name)
        dest_name = file_name[0:-4] + "csv"
        dest_file = os.path.join(target_dir, dest_name)
        xlsx_to_csv(src_file, dest_file)


if __name__ == '__main__':
    xlsx_to_csv_with_dir("./excel_files/")
