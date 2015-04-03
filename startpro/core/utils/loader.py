"""
Created on Dec 2, 2014

@author: Allen
"""

from startpro.common.utils.log4py import log
from startpro.core import settings
from startpro.common.utils.config import Config
import os
import sys
import functools


def load_config(config_file, section):
    """
    load custom configure by section
    """
    config = Config(config_file=config_file)
    settings.CONFIG = config
    for re in config.get_config_list(section):
        setattr(settings, re[0].upper(), re[1])


def get_settings(attr_name, default=None):
    """
    get attribute of settings attribute safety default value
    """
    if hasattr(settings, attr_name.upper()):
        return getattr(settings, attr_name.upper())
    else:
        return default
    
    
def safe_run(func):
    @functools.wraps(func)
    def _deco(*args, **kvargs):
        try:
            func(**kvargs)
        except KeyboardInterrupt:
            print("KeyboardInterrupt.")
            return True
    return _deco


def safe_init_run(func):
    @functools.wraps(func)
    def _deco(*args, **kvargs):
        try:
            loader(**kvargs)
            func(**kvargs)
        except KeyboardInterrupt:
            print("KeyboardInterrupt.")
            return True
    return _deco


def loader(**kwargvs):
    script_name = get_script_name()
    root_path = os.getcwd()
    root_path = kwargvs.get('root_path', root_path)
    # set system context vars
    settings.NAME = script_name
    settings.ROOT_PATH = root_path
    # load configure
    cfg_file = os.path.join(settings.ROOT_PATH, settings.CONFIG_FILE)
    load_config(cfg_file, "common")
    load_config(cfg_file, script_name)
    # init path
    settings.CLIENT_FILE = os.path.join(settings.ROOT_PATH, settings.CLIENT_FILE)
    settings.RESULT_FILE = os.path.join(settings.ROOT_PATH, settings.RESULT_FILE)
    paths = [settings.CLIENT_FILE, settings.RESULT_FILE]
    for path in paths:
        if not os.path.exists(path):
            os.mkdir(path)
    # set log
    log_path = os.path.join(kwargvs.get('log_path', settings.ROOT_PATH), 'log')
    log.set_mail(get_settings('mail_un', ''), get_settings('mail_pw', ''), get_settings('mail_host', ''))
    log.set_mailto([get_settings('mail_to', '')])
    log.set_logfile(script_name, log_path)
    log.info("init context.")
    # set process id
    with open(os.path.join(settings.CLIENT_FILE, "%s.pid" % settings.NAME), 'w') as f:
        f.writelines(["%s" % os.getpid()])
        f.flush()


def get_script_name():
    try:
        script_name = (sys.argv[2])
        script_split = script_name.split('.')
        if len(script_split) > 1:
            script_name = script_split[-2]
        else:
            script_name = script_split[-1]
        return script_name
    except:
        print('[INFO]:Please chose a script.')
        sys.exit(1)