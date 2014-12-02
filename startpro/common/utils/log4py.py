'''
Created on 2013.03.20
@author: Allen
'''
import time
import smtplib
from email.mime.text import MIMEText
import logging.handlers
import os
import socket

FILE_LOG_LEVEL = logging.INFO

CONSOLE_LOG_LEVEL = logging.ERROR

MEMOEY_LOG_LEVEL = logging.ERROR

URGENT_LOG_LEVEL = logging.CRITICAL

host = socket.gethostname()

ERROR_MAIL_SUBJECT = "%s:Too many errors occurred during the execution" % host
ERROR_MESSAGE = 50
CRITICAL_MAIL_SUBJECT = "%s:Fatal error occurred" % host

# mail configure
MAIL_HOST = ""
MAIL_TO = []
MAIL_UN = ""
MAIL_PW = ""

class OptmizedMemoryHandler(logging.handlers.MemoryHandler):
    """
    """
    def __init__(self, capacity, mail_subject):
        logging.handlers.MemoryHandler.__init__(self, capacity, flushLevel=logging.ERROR, target=None)
        self.mail_subject = mail_subject
        self.flushed_buffers = []
        
    def shouldFlush(self, record):
        """
        if reach max
        """
        if len(self.buffer) >= self.capacity:
            return True
        else:
            return False
        
    def flush(self):
        """
        """
        if self.buffer != [] and len(self.buffer) >= self.capacity:
            content = ""
            for record in self.buffer:
                message = record.getMessage()
                level = record.levelname
                ctime = record.created
                t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ctime))
                content += t + " " + "*" + level + "* : " + message + "\n"
            self.mailNotification(self.mail_subject, content)
            self.flushed_buffers.extend(self.buffer)
            self.buffer = []
            
    def mailNotification(self, subject, content):
        if MAIL_TO and MAIL_UN and MAIL_PW and MAIL_HOST:
            """
            """
            msg = MIMEText(content)
            msg['Subject'] = subject
            msg['From'] = MAIL_UN
            msg['To'] = ";".join(MAIL_TO)
            try:
                s = smtplib.SMTP()
                s.connect(MAIL_HOST)
                # s.set_debuglevel(1)
                s.login(MAIL_UN, MAIL_PW)
                s.sendmail(MAIL_UN, MAIL_TO, msg.as_string())
                s.close()
            except:
                pass


class Log:
    """
    """
    def __init__(self, log_name=None, root_path='./'):
        if log_name:
            self.set_logfile(log_name, root_path)
    
    def set_logfile(self, log_name, log_path='./'):
        # log_path = os.path.join(root_path, 'log')
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        log_file = '%s.log' % (log_name)
        log_file = os.path.join(log_path, log_file)
        self.config(log_file, FILE_LOG_LEVEL, CONSOLE_LOG_LEVEL, MEMOEY_LOG_LEVEL, URGENT_LOG_LEVEL)
    
    def set_mail(self, mail_un, mail_pw, mail_host):
        '''
        set mail server configure
        '''
        global MAIL_UN, MAIL_PW, MAIL_HOST
        MAIL_UN = mail_un
        MAIL_PW = mail_pw
        MAIL_HOST = mail_host
    
    def set_mailto(self, mail_to):
        '''
        set mail to
        '''
        global MAIL_TO
        if isinstance(mail_to, str) or isinstance(mail_to, unicode):
            MAIL_TO = [mail_to]
        elif isinstance(mail_to, list):
            MAIL_TO = mail_to
        else:
            pass    
    
    def config(self, logFile, file_level, console_level, memory_level, urgent_level):
        # logger configure
        self.logger = logging.getLogger('root')
        self.logger.setLevel(file_level)
        self.fh = logging.handlers.RotatingFileHandler(logFile, mode='a', maxBytes=1024 * 1024 * 10, backupCount=10, encoding="utf-8")
        self.fh.setLevel(file_level)
        self.ch = logging.StreamHandler()
        self.ch.setLevel(console_level)  
        self.mh = OptmizedMemoryHandler(ERROR_MESSAGE, ERROR_MAIL_SUBJECT)
        self.mh.setLevel(memory_level)
        self.sh = logging.handlers.SMTPHandler(MAIL_HOST, MAIL_UN, ";".join(MAIL_TO), CRITICAL_MAIL_SUBJECT)
        self.sh.setLevel(urgent_level)
        # log format
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] : %(message)s", '%Y-%m-%d %H:%M:%S')
        self.ch.setFormatter(formatter)  
        self.fh.setFormatter(formatter)
        self.mh.setFormatter(formatter)
        self.sh.setFormatter(formatter)
        # add handle
        self.logger.addHandler(self.ch)  
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.mh)
        self.logger.addHandler(self.sh)

    def debug(self, msg):
        if msg is not None:
            self.logger.debug(msg)
            
    def info(self, msg):
        if msg is not None:
            self.logger.info(msg)
            
    def warn(self, msg):
        if msg is not None:
            self.logger.warning(msg)
            
    def error(self, msg):
        if msg is not None:
            self.logger.error(msg)
            
    def critical(self, msg):
        if msg is not None:
            self.logger.critical(msg)

log = Log()
