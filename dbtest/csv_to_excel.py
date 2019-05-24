# encoding: utf-8
import os
import sys
import pandas as pd


def csv_to_xlsx(src_file, dest_file):
    csv_file = pd.read_csv(src_file, encoding="utf-8")
    csv_file.to_excel(dest_file, index=False)


def csv_to_xlsx_with_dir(target_dir):
    for file_name in os.listdir(target_dir):
        if not file_name.endswith('.csv'):
            continue
        src_file = os.path.join(target_dir, file_name)
        dest_name = file_name[0:-3] + "xlsx"
        dest_file = os.path.join(target_dir, dest_name)
        csv_to_xlsx(src_file, dest_file)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print "please input directory to transfer."
        exit(0)
    for i in range(1, len(sys.argv)):
        if os.path.isdir(sys.argv[i]):
            csv_to_xlsx_with_dir(sys.argv[i])
        else:
            print "[%s] is not a dir." % sys.argv[i]
