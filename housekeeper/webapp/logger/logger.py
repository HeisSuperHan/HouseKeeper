
# import logging
#
# class logger():
#
#     def __init__(self):
#         self.logger = logging.getLogger('Flask')
#         self.logger.setLevel(logging.INFO)
#         self.fh = logging.FileHandler('../log_file/webapp.log')
#         self.fh.setLevel(logging.INFO)
#         self.fmt = '[flask:] - %(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s'
#         self.dmt = '%a %d %b %Y %H:%M:%S'
#         self.formatter = logging.Formatter(self.fmt,self.dmt)
#         self.fh.setFormatter(self.formatter)
#         self.logger.addHandler(self.fh)
#
#
#     def log_info(self,msg):
#         self.logger.info(msg)
#
#
#     def log_warn(self,msg):
#         self.logger.warning(msg)
#
#
#     def log_error(self,msg):
#         self.logger.error(msg)

import time

def logger(log_type,logged):
    with open('log/log.txt','a') as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        f.write(' [-] ')
        f.write(log_type)
        f.write(' [-] ')
        f.write(str(logged))
        f.write('\n')
















