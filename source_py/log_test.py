import os
import logging, logging.handlers
import time
import log_init


if __name__ == '__main__':
    log_init.log_init.log_init("log_test", logging.INFO)
    for i in range(0, 10):
        logging.debug("logging.debug")
        logging.info("logging.info")
        logging.warning("logging.warning")
        logging.error("logging.error")
        time.sleep(10)
