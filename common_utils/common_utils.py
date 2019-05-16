# encoding:utf-8


def try_gbk2utf8(gbk):
    try:
        return gbk.decode('gbk').encode('utf-8')
    except:
        return gbk


def trim_return(line):
    return line.replace("\r", "").replace("\n", "").strip()


def transfer_decimal(num):
    num_str = str(float(num))
    if num_str.endswith(".0"):
        num_str = num_str[:-2]
    return num_str

