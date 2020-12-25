import os
import time
import logging, logging.handlers


def log_init(filename='default', loglevel = logging.DEBUG):
    if not os.path.exists("./log"):
        os.mkdir("./log")
    fmt_str = "%(asctime)s %(levelname)8s: %(message)s - %(filename)s:%(lineno)d"
    date_fmt_str = "%Y%m%d %H:%M:%S"
    logging.basicConfig(level=loglevel, filemode="w", format=fmt_str, datefmt=date_fmt_str)

    filename = './log/' + filename + '.log'
    fileshandle = logging.handlers.TimedRotatingFileHandler(filename, when='MIDNIGHT', interval=1, backupCount=30)
    fileshandle.suffix = "%Y%m%d.log"
    fileshandle.setLevel(loglevel)
    formatter = logging.Formatter(fmt=fmt_str, datefmt=date_fmt_str)
    fileshandle.setFormatter(formatter)
    logging.getLogger('').addHandler(fileshandle)
