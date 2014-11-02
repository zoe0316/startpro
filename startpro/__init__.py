# encoding: utf-8

import os
import sys
import re
import pkgutil
import shutil
from importlib import import_module
from shutil import ignore_patterns


__version__ = pkgutil.get_data(__package__, 'VERSION').strip()
if not isinstance(__version__, str):
    __version__ = __version__.decode('ascii')

options = {'-script': 'execute module name.',
           }

MAIN_PATH = "startpro"
MAIN_PY = 'startpro.py'
MAIN_SETTING = os.path.join('core', 'settings.py')

def _get_opts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0][1:]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

def _print_header():
    print("Startpro %s\n" % (__version__))

def _print_commands():
    _print_header()
    print("Usage:")
    print("  startpro [options] [args]\n")
    print("Available commands:")
    for name, desc in sorted(options.iteritems()):
        print("  %-13s %s" % (name, desc))
    print('')

def _startpro(name, opts):
    # root_path = os.path.dirname(sys.argv[0])
    root_path = os.getcwd()
    script_name = opts.get('script', 'script')
    mod = import_module(MAIN_PATH)
    src = mod.__path__[0]
    dst = os.path.join(root_path, name)
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

def execute():
    opts = _get_opts(sys.argv)
    try:
        name = sys.argv[1]
        _startpro(name, opts)
    except:
        _print_commands()
        print("[WARN]:please type a project name.")
        sys.exit()
    