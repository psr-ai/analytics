import logging, datetime
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

logging.error(str(datetime.datetime.now()) + ' This message should go to the log file')