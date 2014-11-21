# encoding: utf8

'''
Created on 2014.06.24

@author: ZoeAllen
'''
import os
from importlib import import_module
import sys

def scan_path(root_path, ends='.py'):
    py_files = []
    full_paths = []
    for root, _, files in os.walk(root_path):
        for f in files:
            if f.endswith(ends) and not f.startswith('__init__'):
                py_files.append(f)
                full_paths.append(os.path.join(root, f))
    return py_files, full_paths

def get_include(file_paths):
    includes = set()
    for path in file_paths:
        mod = import_module(path.replace('.py', '').replace('/', '.'))
        includes.add("import %s" % mod.__name__)
    return list(includes)

def update_main(main_py, res):
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
        
if __name__ == '__main__':
    main_py = sys.argv[1]
    print('[INFO]:load main PY file:%s' % main_py)
    res = []
    for path in sys.argv[ 2: ]:
        print('[INFO]:start scan path:%s' % path)
        py_files, full_paths = scan_path(path)
        res.extend(get_include(full_paths))
    update_main(main_py, res)
    
    