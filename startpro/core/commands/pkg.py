# encoding: utf-8

"""
Created on 2014.05.26

@author: Allen
"""
import os
import shutil
import sys
from collections import OrderedDict
from startpro.core.topcmd import TopCommand
from importlib import import_module
from startpro.core.settings import MAIN_PATH, TEMPLATE_PACKAGE
from startpro.core import settings
from startpro.core.utils.opts import load_script_temp

options = OrderedDict()
options['-name'] = "main package name",
options['-i'] = "package functions include(if more than one, split by comma)"
options['-e'] = "package functions exclude(if more than one, split by comma)"

SPEC_CONTENT = '''
# -*- mode: python -*-
a = Analysis(['#PY_NAME#'],
             pathex=['#PATHEX#'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
             
pyz = PYZ(a.pure)

a.datas = #DATA_FILE#

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='#PKG_NAME#',
          debug=False,
          strip=None,
          upx=True,
          console=True )
'''


class Command(TopCommand):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def run(self, **kwargvs):
        try:
            mod = import_module(MAIN_PATH)
            src = mod.__path__[0]
            path = os.path.join(src, TEMPLATE_PACKAGE)
            name = kwargvs.get('name', None)
            if not name:
                if settings.CONFIG:
                    name = settings.CONFIG.get_config('package', 'name')  # @UndefinedVariable
            if not name:
                return
            PY_NAME = "%s.py" % name
            PATHEX = os.getcwd()
            # main PY
            dst = os.path.join(PATHEX, PY_NAME)
            shutil.copyfile(path, dst)
            patterns = []
            include_regex = [(r, True) for r in filter(lambda x: x, kwargvs.get('i', '').split(','))]
            exclude_regex = [(r, False) for r in filter(lambda x: x, kwargvs.get('e', '').split(','))]
            patterns.extend(include_regex)
            patterns.extend(exclude_regex)
            if patterns:
                load_paths = []
                scripts = load_script_temp()
                for k, v in scripts.items():
                    for r, b in patterns:
                        p = v.get('path')
                        n = v.get('name')
                        if r in p or r in n:
                            if b:
                                load_paths.append(p)
                                break
                            else:
                                break
            else:
                load_paths = kwargvs['load_paths']
            for r in load_paths:
                print('include:[%s]' % r)
            self.update(dst, ["import %s" % r for r in load_paths])
            # configure
            cfg = os.path.join(PATHEX, settings.MAIN_CONFIG)
            settings.CONFIG.set_config("package", "load", str(kwargvs.get('paths', '')))  # @UndefinedVariable
            # PYINSTALLER
            PKG_NAME = name
            DATA_FILE = []
            DATA_FILE.append(('/startpro/VERSION', os.path.join(src, 'VERSION'), 'DATA'))
            DATA_FILE.append(('/startpro/startpro.cfg', cfg, 'DATA'))
            DATA_FILE.append(('/startpro/template/package.py', path, 'DATA'))
            global SPEC_CONTENT
            SPEC_CONTENT = SPEC_CONTENT.replace("#PY_NAME#", PY_NAME).replace("#PATHEX#", PATHEX). \
                replace("#DATA_FILE#", str(DATA_FILE)).replace("#PKG_NAME#", PKG_NAME)
            spec = dst.replace(".py", ".spec")
            with open(spec, 'w') as f:
                f.write(SPEC_CONTENT)
                f.flush()
            os.system("pyinstaller -F %s" % spec)
            settings.CONFIG.remove_option("package", "load")  # @UndefinedVariable
            # os.remove(spec)
            print("[INFO]:package:[%s]" % os.path.join(os.path.join(PATHEX, "dist"), PKG_NAME))
        except Exception, e:
            print("[ERROR]:%s" % e)
            s = sys.exc_info()
            print('pkg %s on line %d.' % (s[1], s[2].tb_lineno))

    def update(self, main_py, res):
        lines = []
        start = False
        end = False
        with open(main_py, 'r') as f:
            for line in f:
                if line.startswith("# [LOAD MODULE END]"):
                    end = True
                if not start:
                    lines.append(line)
                else:
                    if end:
                        lines.append(line)
                if line.startswith("# [LOAD MODULE START]"):
                    start = True
                    lines.append("%s\n" % "\n".join(res))
        with open(main_py, 'w') as f:
            f.writelines("".join(lines))
            f.flush()

    def help(self, **kwargvs):
        print('')
        print("Available options:")
        for name, desc in sorted(options.iteritems()):
            print("  %-13s %s" % (name, desc))
