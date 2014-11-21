# encoding: utf-8

import os
import sys
import re
import pkgutil
import shutil
from importlib import import_module
from shutil import ignore_patterns
from common.utils.config import Config
from core.utils.opts import get_command
from core import settings
from core.utils.opts import load_modeule_auto
import glob

# [LOAD MODULE START]
import core.commands.start
import core.commands.list
import core.commands.create
# [LOAD MODULE END]

from core.settings import MAIN_PY, MAIN_CONFIG, MAIN_PATH, MAIN_SETTING


__version__ = pkgutil.get_data(__package__, 'VERSION').strip()
if not isinstance(__version__, str):
    __version__ = __version__.decode('ascii')


def _get_opts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            if len(argv) > 1:
                opts[argv[0][1:]] = argv[1]  # Add key and value to the dictionary.
            else:
                opts[argv[0][1:]] = None
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
        
    return opts


def _print_header():
    print("Startpro %s\n" % (__version__))


def _print_commands(commands=None):
    _print_header()
    print("Usage:")
    print("  startpro command [-options] [option_value]\n")
    if commands:
        print("Available command:")
        for name in sorted(commands.keys()):
            print("  %s" % (name))
    print('')


def _include(src, dst, script_name, name):
    try:
        shutil.copytree(src, dst, ignore=ignore_patterns('*.pyc', "VERSION"))
        os.rename(os.path.join(dst, MAIN_PY), os.path.join(dst, "%s.py" % name))
        try:
            os.remove(os.path.join(dst, '__init__.py'))
        except:
            pass
        f = os.path.join(dst, MAIN_SETTING)
        res = re.sub(r"%SCRIPT_MODULE_FLAG%", "%s" % script_name, open(f).read())
        with open(f, 'w') as setting_f:
            setting_f.write(res)
        f = os.path.join(dst, "script")
        os.rename(f, os.path.join(dst, script_name))
        f = os.path.join(dst, "package.sh")
        with open(f, 'w') as sh_f:
            sh_f.write("python pkg.py %s.py core/commands %s" % (name, script_name))
    except OSError:
        print("[Errno 17] File exists: '%s'" % name)
    
    
def _create(opts):
    try:
        # root_path = os.path.dirname(sys.argv[0])
        if 'name' not in opts:
            _print_commands()
            print("[WARN]:create argument [ -name ] optional.")
            return None
        root_path = os.getcwd()
        name = opts['name']
        script_name = opts.get('script', 'script')
        include = opts.get('include', '')
        mod = import_module(MAIN_PATH)
        src = mod.__path__[0]
        dst = os.path.join(root_path, name)
        if include == "all":
            _include(src, dst, script_name, name)
        else:
            pass
    except Exception, e:
        print(e)


def _start():
    try:
        root_path = os.getcwd()
        path = os.path.join(root_path, MAIN_CONFIG)
        if not os.path.exists(path):
            print("[WARN]:[%s] not found." % path)
            return
        config = Config(path)
        script = config.get_config('settings', 'default')
        if script:
            return script
        else:
            print("[WARN]:[%s] not found in [%s]." % ('default script module name' , path))
            return
    except Exception, e:
        print(e)


def execute():
    try:
        cmds = get_command([settings.COMMAND_MODEULE])
        if len(sys.argv) > 1:
            curr_path = os.getcwd()
            sys.path.append(curr_path)
            match = _start()
            paths = []
            for m in match.split(","):
                for re in glob.glob(os.path.join(curr_path, m)):
                    paths.append(os.path.basename(re))
            load_modeule_auto(curr_path, paths)
            opts = _get_opts(sys.argv)
            opts['paths'] = paths
            name = sys.argv[1]
            func = cmds.get(name)
            if func:
                if "help" in opts or "-help" in opts:
                    func.help(**opts)
                    return
                func.run(**opts)
        else:
            _print_commands(cmds)
    except:
        s = sys.exc_info()
        msg = u'execute %s happened on line %d' % (s[1], s[2].tb_lineno)
        print msg
        _print_commands(cmds)
        sys.exit()
    