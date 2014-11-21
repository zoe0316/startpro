# encoding: utf-8

'''
@author: Allen
'''
import sys
from startpro.common.utils.log4py import log
import os
from startpro.core import settings
from startpro.core.utils.opts import get_command, get_opts, load_config, get_attr

# [LOAD MODULE START]
import startpro.core.commands.start
import startpro.core.commands.list
# [LOAD MODULE END]

reload(sys)
sys.setdefaultencoding('utf8')  # @UndefinedVariable

def _get_name():
    try:
        script_name = (sys.argv[2])
        log_name = script_name
        script_split = script_name.split('.')
        if len(script_split) > 1:
            log_name = script_split[-2]
        else:
            log_name = script_split[-1]
        return log_name
    except:
        print('[INFO]:Please chose a script.')
        sys.exit(1)

def start():
    cmds = get_command()
    for cmd in cmds:
        print('----> %s' % cmd)
        
    if len(sys.argv) >= 2:
        program = str(sys.argv[1])
    else:
        print('[WARN]:need sys.argv[1],exit.')
        sys.exit()

    kwargvs = get_opts(sys.argv)
    
    if program == 'start':
        log_name = _get_name()
        try:
            root_path = os.path.dirname(sys.argv[0])
            # set system context vars
            settings.NAME = program
            settings.ROOT_PATH = kwargvs.get('root_path', root_path)
            # set log
            log_path = os.path.join(kwargvs.get('log_path', settings.ROOT_PATH), 'log')
            log.set_logfile(log_name, log_path)
            for re in kwargvs.items():
                setattr(settings, re[0].upper(), re[1])
            # INIT path
            settings.CLIENT_FILE = os.path.join( settings.ROOT_PATH, settings.CLIENT_FILE )
            settings.RESULT_FILE = os.path.join( settings.ROOT_PATH, settings.RESULT_FILE )
            paths = [settings.CLIENT_FILE, settings.RESULT_FILE]
            for path in paths:
                if not os.path.exists(path):
                    os.mkdir(path)
            # load common configure
            load_config(os.path.join(root_path, settings.CONFIG_FILE), "common")
            # load custom configure
            load_config(os.path.join(root_path, settings.CONFIG_FILE), log_name)
            # set log mail configure
            log.set_mail(get_attr('mail_un', ''), get_attr('mail_pw', ''))
            log.set_mailto([ get_attr('mail_to', []) ])
        except Exception, e:
            print '[ERROR]:Init syscontext error:%s' % str(e)
            sys.exit()
    
    if cmds.has_key(program):
        cmd = cmds.get(program)
        cmd.run(program = program, opts = kwargvs)
    else:
        print('Unsupported process.')

if __name__ == '__main__':
    start()
    print('[INFO]:End.')
