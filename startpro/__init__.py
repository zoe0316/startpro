# encoding: utf-8

'''
Created on 2014.05.26

@author: Allen
'''

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
from core.utils.opts import load_modeule_auto, _get_opts
import glob

# [LOAD MODULE START]
import core.commands.start
import core.commands.list
import core.commands.create
import core.commands.pkg
# [LOAD MODULE END]

import json

__version__ = pkgutil.get_data(__package__, 'VERSION').strip()
if not isinstance(__version__, str):
    __version__ = __version__.decode('utf8')


def _print_header():
    print("Startpro %s\n" % (__version__))

def _print_commands(commands=None):
    _print_header()
    print("Usage:")
    print("\tstartpro command [-options] [option_value]\n")
    if commands:
        print("Available command:")
        for name in sorted(commands.keys()):
            print("  %s" % (name))
    print('')

def _include(src, dst, script_name, name):
    try:
        shutil.copytree(src, dst, ignore=ignore_patterns('*.pyc', "VERSION"))
        os.rename(os.path.join(dst, settings.MAIN_PY), os.path.join(dst, "%s.py" % name))
        try:
            os.remove(os.path.join(dst, '__init__.py'))
        except:
            pass
        f = os.path.join(dst, settings.MAIN_SETTING)
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
        mod = import_module(settings.MAIN_PATH)
        src = mod.__path__[0]
        dst = os.path.join(root_path, name)
        if include == "all":
            _include(src, dst, script_name, name)
        else:
            pass
    except Exception, e:
        print(e)

def _start(root_path):
    try:
        path = os.path.join(root_path, settings.MAIN_CONFIG)
        if not os.path.exists(path):
            print("[WARN]:[%s] not found." % path)
            return
        config = Config(path)
        settings.CONFIG = config
        script = config.get_config('settings', 'default')
        if script:
            return script
        else:
            print("[WARN]:[%s] not found in [%s]." % ('default script module name' , path))
            return
    except Exception, e:
        print(e)

def pkg_run(curr_path, opts):
    match = _start(curr_path)
    # print curr_path
    paths = settings.CONFIG.get_config("package", "load")
    paths = json.loads(paths.replace("'", '"'))
    # load_paths = load_modeule_auto("", paths)
    opts['paths'] = paths
    opts['load_paths'] = paths
    return match

def normal_run(curr_path, opts):
    match = _start(curr_path)
    paths = []
    for m in match.split(","):
        for re in glob.glob(os.path.join(curr_path, m)):
            paths.append(os.path.basename(re))
    load_paths = load_modeule_auto(curr_path, paths)
    opts['paths'] = paths
    opts['load_paths'] = load_paths
    return match

def execute(pkg=False):
    try:
        cmds = get_command([settings.COMMAND_MODEULE])
        if len(sys.argv) > 1:
            name = sys.argv[1]
            opts = _get_opts(sys.argv)
            func = cmds.get(name)
            if not func:
                print("[INFO]:Unsupported command.\n")
                _print_commands(cmds)
                return
            curr_path = os.getcwd()
            sys.path.append(curr_path)
            if "create" != name:
                if pkg:
                    if not pkg_run(__path__[0], opts): return
                else:
                    if not normal_run(curr_path, opts): return 
            if "help" in opts or "-help" in opts or "--help" in opts:
                func.help(**opts)
                return
            func.run(**opts)
        else:
            _print_commands(cmds)
    except:
        s = sys.exc_info()
        msg = u'[ERROR]:execute [%s] happened on line %d' % (s[1], s[2].tb_lineno)
        print(msg)
