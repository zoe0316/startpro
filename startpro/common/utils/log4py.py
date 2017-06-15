"""
Created on 2013.03.20
@author: Allen
"""
import os
import sys
import time
import socket
import smtplib
import logging.handlers
from collections import deque
from email.mime.text import MIMEText

FILE_LOG_LEVEL = logging.INFO

CONSOLE_LOG_LEVEL = logging.ERROR

MEMOEY_LOG_LEVEL = logging.ERROR

URGENT_LOG_LEVEL = logging.CRITICAL

host = socket.gethostname()

ERROR_MAIL_SUBJECT = "%s:Too many errors occurred during the execution" % host

# error log count to send notify
ERROR_MESSAGE = 50

# seconds for keep log error time window to send notify
# 0: forever
ERROR_MESSAGE_WINDOW = 0

CRITICAL_MAIL_SUBJECT = "%s:Fatal error occurred" % host

# mail configure
MAIL_HOST = ""
MAIL_TO = []
MAIL_UN = ""
MAIL_PW = ""

# log format
FMT_DATE = '%Y-%m-%d %H:%M:%S'
FMT_LINE = '%(asctime)-15s [%(levelname)s] p:[%(process)d] file:[%(pathname)s] line:[%(lineno)d] %(message)s'


class OptmizedMemoryHandler(logging.handlers.MemoryHandler):
    """
    """

    def __init__(self, capacity, mail_subject):
        logging.handlers.MemoryHandler.__init__(self, capacity, flushLevel=logging.ERROR, target=None)
        self.mail_subject = mail_subject
        self.buffer = deque(maxlen=ERROR_MESSAGE)

    def emit(self, record):
        """
        Emit a record.

        Append the record. If shouldFlush() tells us to, call flush() to process
        the buffer.
        """
        self.buffer.append({'record': record, 'time': int(time.time())})
        if self.shouldFlush(record):
            self.flush()

    def shouldFlush(self, record):
        """
        if reach max
        """
        if len(self.buffer) >= ERROR_MESSAGE:
            if ERROR_MESSAGE_WINDOW:
                # check error time window
                if (self.buffer[-1]['time'] - self.buffer[0]['time']) <= ERROR_MESSAGE_WINDOW:
                    return True
                return False
            return True
        else:
            return False

    def flush(self):
        """
        """
        self.acquire()
        try:
            if self.shouldFlush(None):
                content = []
                for r in self.buffer:
                    record = r['record']
                    msg = self.format(record)
                    content.append(msg)
                if content:
                    self.notify(self.mail_subject, '\n'.join(content))
                # clear buffer
                self.buffer.clear()
        finally:
            self.release()

    @staticmethod
    def notify(subject, content):
        if MAIL_TO and MAIL_UN and MAIL_PW and MAIL_HOST:
            """
            send mail
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
            except Exception:
                s = sys.exc_info()
                msg = '[ERROR]:notify [{}] happened on line {}'.format(s[1], s[2].tb_lineno)
                print(msg)
            finally:
                try:
                    s.close()
                except:
                    pass


class Log:
    """
    startpro log instance
    """

    def __init__(self):
        self.fh = None
        self.ch = None
        self.mh = None
        self.sh = None
        self._formatter = None
        self.logger = logging.getLogger()

    @property
    def formatter(self):
        return self._formatter or logging.Formatter(FMT_LINE, FMT_DATE)

    def set_logfile(self, log_name, log_path='./'):
        """
        set log file path
        and config logger
        :param log_name:
        :param log_path:
        :return:
        """
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        log_file = None
        if log_name:
            # check log file name
            if log_name.endswith('.log'):
                log_file = log_name
            else:
                log_file = '%s.log' % log_name
            log_file = os.path.join(log_path, log_file)
        self.config(log_file, FILE_LOG_LEVEL, CONSOLE_LOG_LEVEL)

    @staticmethod
    def set_mail(mail_un, mail_pw, mail_host):
        """
        set mail server configure
        """
        global MAIL_UN, MAIL_PW, MAIL_HOST
        MAIL_UN = mail_un
        MAIL_PW = mail_pw
        MAIL_HOST = mail_host

    def set_mailto(self, mail_to):
        """
        set mail to, call after set_mail
        """
        global MAIL_TO
        if isinstance(mail_to, str) or isinstance(mail_to, unicode):
            MAIL_TO = [mail_to]
        elif isinstance(mail_to, list):
            MAIL_TO = mail_to
        # set mail configure
        self.mh = OptmizedMemoryHandler(ERROR_MESSAGE, ERROR_MAIL_SUBJECT)
        self.mh.setLevel(MEMOEY_LOG_LEVEL)
        self.sh = logging.handlers.SMTPHandler(MAIL_HOST, MAIL_UN, ";".join(MAIL_TO), CRITICAL_MAIL_SUBJECT)
        self.sh.setLevel(URGENT_LOG_LEVEL)
        self.mh.setFormatter(self.formatter)
        self.sh.setFormatter(self.formatter)
        # add handler
        self.logger.addHandler(self.mh)
        self.logger.addHandler(self.sh)

    def set_error_limit(self, limit=50):
        """

        :param limit: limit size
        :return:
        """
        global ERROR_MESSAGE
        ERROR_MESSAGE = limit
        # update deque max len
        if self.mh:
            self.mh.buffer = deque(maxlen=ERROR_MESSAGE)

    @staticmethod
    def set_error_window(window=0):
        global ERROR_MESSAGE_WINDOW
        ERROR_MESSAGE_WINDOW = window

    def set_log_level(self, log_level=logging.INFO):
        self.logger.setLevel(log_level)

    def config(self, log_file, file_level, console_level):
        """
        set log option
        :param log_file: log file path
        :param file_level: log level
        :param console_level:
        :return:
        """
        # logger configure
        self.logger.setLevel(file_level)
        # log format
        self.ch = logging.StreamHandler()
        self.ch.setLevel(console_level)
        self.ch.setFormatter(self.formatter)
        self.logger.addHandler(self.ch)
        # add handle
        if log_file:
            self.fh = logging.handlers.RotatingFileHandler(
                log_file, mode='a', maxBytes=1024 * 1024 * 10,
                backupCount=10, encoding="utf-8"
            )
            self.fh.setLevel(file_level)
            self.fh.setFormatter(self.formatter)
            self.logger.addHandler(self.fh)

    def debug(self, msg):
        if msg:
            self.logger.debug(msg)

    def info(self, msg):
        if msg:
            self.logger.info(msg)

    def warn(self, msg):
        if msg:
            self.logger.warning(msg)

    def error(self, msg):
        if msg:
            self.logger.error(msg)

    def critical(self, msg):
        if msg:
            self.logger.critical(msg)


base_log = Log()
log = logging.getLogger(__name__)
