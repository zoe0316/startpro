# -*- encoding: utf-8 -*-

"""
Created on 2014.04.16

@author: Allen
"""
from collections import OrderedDict
from importlib import import_module
from inspect import isclass, ismodule, isfunction
import json
import os
import re
import sys

from startpro.core import settings
from startpro.core.process import Process
from startpro.core.topcmd import TopCommand

# uniq module dict to prevent max loop
UNIQ_MODULE = {}


def get_opts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            if len(argv) > 1:
                opts[argv[0][1:]] = argv[1]  # Add key and value to the dictionary.
            else:
                opts[argv[0][1:]] = None
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts


def load_module_auto(root_path, scan_paths):
    paths = set()
    for p in scan_paths:
        for root, _, files in os.walk(import_module(p).__path__[0]):
            for f in files:
                try:
                    if f.startswith("__") or f.endswith("pyc") or not f.endswith(".py"):
                        continue
                    f = os.path.join(root, f)
                    f = f.replace(root_path, "").split(os.path.sep)
                    module_path = ".".join(f)
                    if module_path.startswith("."):
                        module_path = module_path[1: -3]
                    # uniq
                    if module_path in paths:
                        continue
                    paths.add(module_path)
                    import_module(module_path)
                except Exception as e:
                    print("load:[{}], {}".format(module_path, e))
    return list(paths)


def load_module(module_path, match=""):
    """
    Return: [module object] list
    module_path : argument required, package path

    when module in this package starts with settings.COMMAND_MODEULE / settings.SCRIPT_MODULE
    and not inner attribute
    """
    mods = []
    if module_path:
        try:
            # match
            match = [settings.COMMAND_MODEULE]
            config = settings.CONFIG
            if config:
                match.extend(config.get_config('settings', 'default').split(","))
            p = re.compile("|".join(["\A{}".format(r) for r in match]))
            # if not match commands or main scripts
            if not p.match(module_path):
                return mods
            mod = import_module(module_path)
            for module in dir(mod):
                # if module_path.startswith(settings.COMMAND_MODEULE) or module_path.startswith(settings.SCRIPT_MODULE):
                if not module.startswith('__'):
                    mods.append(import_module("{}.{}".format(module_path, module)))
        except Exception as e:
            print("load_module:{} at:{}".format(e, module_path))
    return mods


def __scan_mod(path):
    """
    Return: [{'name': cls.name, 'func': cls.run, 'is_class': True, 'path': item.__module__}] list of dict
    path : argument required, package path

    each package path
    when module in this package is subclass of executable class Process,
    when module in this package starts with 'run'
    """
    res = []

    for mod in load_module(path):
        for item in dir(mod):
            try:
                item = getattr(mod, item)
                # get item id
                item_id = id(item)
                if item_id in UNIQ_MODULE:
                    continue
                # set item to uniq dict
                UNIQ_MODULE[item_id] = None
                if isclass(item) and issubclass(item, Process):
                    cls = item()
                    if hasattr(cls, 'name'):
                        res.append({'name': cls.name, 'func': cls.run, 'is_class': True, 'path': item.__module__})
                        # res.append((cls.name, cls.run, True, item.__module__))
                elif ismodule(item):
                    res.extend(__scan_mod(item.__package__))
                else:
                    if isfunction(item) and item.__name__.startswith('run'):
                        func_name = "%s.%s" % (mod.__name__, item.__name__)
                        res.append({'name': func_name, 'func': item, 'is_class': False, 'path': mod.__name__})
                        # res.append((func_name, item, False, mod.__name__))
            except Exception:
                s = sys.exc_info()
                print("scan_mod {} on line {}".format(s[1], s[2].tb_lineno))

    return res


def get_script(paths, full=False, choose=None):
    """
    Return: dict of executable script name
    """
    mapping = {}
    for p in paths:
        for r in __scan_mod(p):
            name = r.get('name')
            if full or name.find(".") < 0 or r.get('is_class'):
                mapping[name] = r
            else:
                mapping[".".join(name.split(".")[1:])] = r
    # filter
    if choose:
        for key in set(mapping.keys()):
            if key.split(".")[0] not in choose.split(','):
                del(mapping[key])
    # save script list to temp file
    save_script_temp(mapping)
    return mapping


def get_command(paths):
    """
    Return: dict of commands
    """
    mapping = {}
    for p in paths:
        for mod in load_module(p):
            for item in dir(mod):
                if item == 'TopCommand':
                    continue
                item = getattr(mod, item)
                if isclass(item) and issubclass(item, TopCommand):
                    mapping[mod.__name__.split('.')[-1]] = item()
    return mapping


def save_script_temp(mapping):
    """
    save script list to temp file
    :param res:
    :return:
    """
    try:
        path = os.path.join(os.getcwd(), settings.SCRIPT_TEMP)
        with(open(path, 'w+')) as tmp_file:
            for k in sorted(mapping.keys()):
                v = mapping.get(k)
                v['name'] = k
                try:
                    del v['func']
                except:
                    pass
                tmp_file.write('%s\n' % (json.dumps(v)))
            tmp_file.flush()
    except Exception:
        s = sys.exc_info()
        print('ERROR:save_script_temp %s on line %d' % (s[1], s[2].tb_lineno))


def load_script_temp():
    """
    when load script return none
    should we auto create a script temp file? just remind user to manual execute `startpro list`
    :return:
    """
    path = os.path.join(os.getcwd(), settings.SCRIPT_TEMP)
    if not os.path.exists(path):
        return
    scripts = OrderedDict()
    with(open(path)) as tmp_file:
        for line in tmp_file:
            line = line.strip()
            if not line:
                continue
            line = json.loads(line)
            scripts[line.get('name')] = line
    return scripts


def get_exec_func(mod, name, is_class=True):
    func = None
    for item in dir(mod):
        if item.startswith('__'):
            continue
        item = getattr(mod, item)
        if is_class:
            if isclass(item) and issubclass(item, Process):
                cls = item()
                if hasattr(cls, 'name') and cls.name.endswith(name):
                    func = cls.run
        else:
            name = name.split('.')[-1]
            if isfunction(item) and item.__name__ == name:
                func = item
    return func
