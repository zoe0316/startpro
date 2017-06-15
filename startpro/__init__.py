# encoding: utf-8

"""
Created on 2014.05.26

@author: Allen
"""
from __future__ import absolute_import

import os
import sys
import re
import pkgutil
import shutil
import platform
from importlib import import_module
from shutil import ignore_patterns
import glob

from startpro.common.utils.config import Config
from startpro.core.utils.opts import get_command
from startpro.core import settings
from startpro.core.utils.opts import load_module_auto, get_opts

# [LOAD MODULE START]
import startpro.core.commands.start
import startpro.core.commands.list
import startpro.core.commands.create
import startpro.core.commands.pkg
# [LOAD MODULE END]

import json

if sys.version_info < (3, 4):
    # compatible with python 2
    reload(sys)
    sys.setdefaultencoding('utf8')  # @UndefinedVariable


__version__ = pkgutil.get_data('startpro', 'VERSION')
if not isinstance(__version__, str):
    __version__ = __version__.decode('utf8')


def _print_header():
    print("Startpro {}".format(__version__))
    print("Python Version:{}\n".format(platform.python_version()))


def _print_commands(commands=None):
    _print_header()
    print("Usage:")
    print("\tstartpro command [-options] [option_value]\n")
    if commands:
        print("Available command:")
        for name in sorted(commands.keys()):
            print("  {}".format(name))
    print('')


def _include(src, dst, script_name, name):
    try:
        shutil.copytree(src, dst, ignore=ignore_patterns('*.pyc', "VERSION"))
        os.rename(os.path.join(dst, settings.MAIN_PY), os.path.join(dst, "{}.py".format(name)))
        try:
            os.remove(os.path.join(dst, '__init__.py'))
        except:
            pass
        f = os.path.join(dst, settings.MAIN_SETTING)
        res = re.sub(r"%SCRIPT_MODULE_FLAG%", "{}".format(script_name), open(f).read())
        with open(f, 'w') as setting_f:
            setting_f.write(res)
        f = os.path.join(dst, "script")
        os.rename(f, os.path.join(dst, script_name))
        f = os.path.join(dst, "package.sh")
        with open(f, 'w') as sh_f:
            sh_f.write("python pkg.py {}.py core/commands {}".format(name, script_name))
    except OSError:
        print("[Errno 17] File exists: '{}'".format(name))


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
    except Exception as e:
        print(e)


def _start(root_path):
    """
    link to start command
    :param root_path:
    :return:
    """
    try:
        path = os.path.join(root_path, settings.MAIN_CONFIG)
        if not os.path.exists(path):
            print("[WARN]:[{}] not found.".format(path))
            return
        config = Config(path)
        settings.CONFIG = config
        script = config.get_config('settings', 'default')
        if script:
            return script
        else:
            print("[WARN]:[{}] not found in [{}].".format('default script module name', path))
            return
    except Exception as e:
        print(e)


def pkg_run(curr_path, opts):
    """
    for py-installer package run mode only
    :param curr_path:
    :param opts:
    :return:
    """
    match = _start(curr_path)
    paths = settings.CONFIG.get_config("package", "load")
    paths = json.loads(paths.replace("'", '"'))
    # load_paths = load_modeule_auto("", paths)
    opts['paths'] = paths
    opts['load_paths'] = paths
    return match


def normal_run(curr_path, opts):
    """
    command run mode
    :param curr_path:
    :param opts:
    :return:
    """
    match = _start(curr_path)
    paths = []
    for m in match.split(","):
        for r in glob.glob(os.path.join(curr_path, m)):
            paths.append(os.path.basename(r))
    load_paths = load_module_auto(curr_path, paths)
    opts['paths'] = paths
    opts['load_paths'] = load_paths
    return match


def execute(pkg=False):
    """
    main process
    :param pkg:
    :return:
    """
    try:
        cmds = get_command([settings.COMMAND_MODEULE])
        if len(sys.argv) > 1:
            name = sys.argv[1]
            opts = get_opts(sys.argv)
            func = cmds.get(name)
            if not func:
                print("[INFO]:Unsupported command.\n")
                _print_commands(cmds)
                return
            curr_path = os.getcwd()
            sys.path.append(curr_path)
            if name not in ['create', 'start']:
                if pkg:
                    if not pkg_run(__path__[0], opts):
                        return
                else:
                    if not normal_run(curr_path, opts):
                        return
            if "-h" in opts or "-help" in opts or "--help" in opts:
                func.help(**opts)
                return
            func.run(**opts)
        else:
            _print_commands(cmds)
    except Exception:
        s = sys.exc_info()
        msg = '[ERROR]:execute [{}] happened on line {}'.format(s[1], s[2].tb_lineno)
        print(msg)
