# encoding: utf-8

'''
Created on 2014.05.26

@author: Allen
'''
from startpro.core.topcmd import TopCommand
from importlib import import_module
from startpro.core.settings import MAIN_PATH, TEMPLATE_PACKAGE
import os
from startpro.core import settings
import shutil

options = {'-name': "main package name"}

SPEC_CONTENT='''
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
            load_paths = kwargvs['load_paths']
            self.update(dst, [ "import %s" % re for re in load_paths ])
            # configure
            cfg = os.path.join(PATHEX, settings.MAIN_CONFIG)
            settings.CONFIG.set_config("package", "load", str(kwargvs.get('paths', '')))  # @UndefinedVariable
            # PYINSTALLER
            PKG_NAME = name
            DATA_FILE = []
            DATA_FILE.append( ('/startpro/VERSION', os.path.join(src, 'VERSION'), 'DATA') )
            DATA_FILE.append( ('/startpro/startpro.cfg', cfg, 'DATA') )
            DATA_FILE.append( ('/startpro/template/package.py', path, 'DATA') )
            global SPEC_CONTENT
            SPEC_CONTENT = SPEC_CONTENT.replace("#PY_NAME#", PY_NAME).replace("#PATHEX#", PATHEX).\
                            replace("#DATA_FILE#", str(DATA_FILE)).replace("#PKG_NAME#", PKG_NAME)
            spec = dst.replace(".py", ".spec")
            with open(spec, 'w') as f:
                f.write(SPEC_CONTENT)
                f.flush()
            os.system("pyinstaller -F %s" % spec)
            settings.CONFIG.remove_option("package", "load")  # @UndefinedVariable
            os.remove(spec)
            print("[INFO]:package:[%s]" % os.path.join(os.path.join(PATHEX, "dist"), PKG_NAME))
        except Exception, e:
            print("[ERROR]:%s" % e)
        
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
        