# encoding: utf-8

"""
Created on 2014.05.26

@author: Allen
"""
import sys
from importlib import import_module

from startpro.core.topcmd import TopCommand
from startpro.core.utils.opts import load_script_temp, get_exec_func

options = {"-full": "if need full path name of script"}


class Command(TopCommand):
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """

    def run(self, **kwargvs):
        if len(sys.argv) < 3:
            print('[WARN]:need start script name.')
            return
        script_name = str(sys.argv[2])
        scripts = load_script_temp()
        if not scripts:
            print('[INFO]:please execute command [startpro list] first')
            return
        try:
            if script_name.isdigit() and script_name not in scripts:
                script_name = scripts.keys()[int(script_name)]
            if script_name not in scripts:
                raise RuntimeError('Unsupported script')
        except Exception:
            print('[ERROR]:Unsupported script.')
            return
        script = scripts[script_name]
        mod = import_module(script['path'])
        func = get_exec_func(mod=mod, name=script_name, is_class=script['is_class'])
        func(**kwargvs)

    def help(self, **kwargvs):
        print('Start a program.')
        print('')
        print("Available options:")
        for name, desc in sorted(options.items()):
            print("  %-13s %s" % (name, desc))
