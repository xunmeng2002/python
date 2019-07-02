# encoding:utf-8


def try_gbk2utf8(gbk):
    try:
        return gbk.decode('utf8').encode('utf8')
    except:
        return gbk.decode('gbk').encode('utf8')


def trim_return(line):
    return line.replace("\r", "").replace("\n", "").strip()


def transfer_decimal(num):
    return ("%.10f" % float(num)).rstrip('0').rstrip('.')
