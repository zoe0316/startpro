# encoding: utf-8

"""
Created on 2014.05.26

@author: Allen
"""
import os
import sys
import shutil

from collections import OrderedDict
from importlib import import_module

from startpro.core.topcmd import TopCommand
from startpro.core.settings import MAIN_PATH, TEMPLATE_PACKAGE
from startpro.core import settings
from startpro.core.utils.opts import load_script_temp

options = OrderedDict()
options['-name'] = "main package name",
options['-i'] = "package functions include(if more than one, split by comma)"
options['-e'] = "package functions exclude(if more than one, split by comma)"
# fix to hooks collect
options['-add-data'] = "py-installer add-data string [such:'SRC:DEST,SRC:DEST']"

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
    def __init__(self):
        """
        Constructor
        """

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
            py_name = "%s.py" % name
            path_ex = os.getcwd()
            # main PY
            dst = os.path.join(path_ex, py_name)
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
            cfg = os.path.join(path_ex, settings.MAIN_CONFIG)
            settings.CONFIG.set_config("package", "load", str(kwargvs.get('paths', '')))  # @UndefinedVariable
            # py installer
            pkg_name = name
            data_file = [
                ('/startpro/VERSION', os.path.join(src, 'VERSION'), 'DATA'),
                ('/startpro/startpro.cfg', cfg, 'DATA'),
                ('/startpro/template/package.py', path, 'DATA')
            ]
            # update extend hooks
            more_file = kwargvs.get('add-data', '').strip()
            # parse add-file
            if more_file:
                for r in more_file.split(','):
                    r = r.split(':')
                    data_file.append((r[1], r[0], 'DATA'))
            global SPEC_CONTENT
            SPEC_CONTENT = SPEC_CONTENT.replace("#PY_NAME#", py_name).replace("#PATHEX#", path_ex). \
                replace("#DATA_FILE#", str(data_file)).replace("#PKG_NAME#", pkg_name)
            spec = dst.replace(".py", ".spec")
            with open(spec, 'w') as f:
                f.write(SPEC_CONTENT)
                f.flush()
            os.system("pyinstaller -F {}".format(spec))
            settings.CONFIG.remove_option("package", "load")
            # os.remove(spec)
            print("[INFO]:package:[%s]" % os.path.join(os.path.join(path_ex, "dist"), pkg_name))
        except Exception as e:
            print("[ERROR]:%s" % e)
            s = sys.exc_info()
            print('pkg %s on line %d.' % (s[1], s[2].tb_lineno))

    @staticmethod
    def update(main_py, res):
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
        for name, desc in sorted(options.items()):
            print("  %-13s %s" % (name, desc))
