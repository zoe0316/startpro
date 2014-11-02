#-*- encoding: utf-8 -*-

'''
Created on 2014.04.16

@author: ZoeAllen
'''
from importlib import import_module
from inspect import isclass, ismodule, isfunction
from core import settings
from core.process import Process
from core.topcmd import TopCommand
from common.utils.config import Config
from common.utils.log4py import log

def get_opts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0][1:]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

def load_module(module_path):
    '''
    Return: [module object] list
    module_path : argument required, package path
    
    when module in this package starts with settings.COMMAND_MODEULE
    when module in this package starts with settings.SCRIPT_MODULE
    and not inner attribute
    '''
    mods = []
    if module_path:
        mod = import_module(module_path)
        for module in dir(mod):
            if module_path.startswith(settings.COMMAND_MODEULE) or module_path.startswith(settings.SCRIPT_MODULE):
                if not module.startswith('__'):
                    mods.append(import_module("%s.%s" % (module_path, module)))
    return mods

def __scan_mod(path):
    '''
    Return: [(name, class or function) ] list of tuple
    path : argument required, package path
    
    each package path
    when module in this package is subclass of executable class Process,
    when module in this package starts with 'run'
    '''
    res = []
    for mod in load_module(path):
        for item in dir(mod):
            item = getattr(mod, item)
            if isclass(item) and issubclass(item, Process):
                cls = item()
                if hasattr(cls, 'name'):
                    res.append( (cls.name, cls.run) )
            elif ismodule(item):
                res.extend(__scan_mod(item.__package__))
            else:
                if isfunction(item) and item.__name__.startswith('run') and mod.__name__.startswith(settings.SCRIPT_MODULE):
                    func_name = "%s.%s" % (mod.__name__, item.__name__)
                    res.append( (func_name, item) )
    return res
    
def get_script():
    '''
    Return: dict of executable script name 
    '''
    mapping = {}
    for re in __scan_mod(settings.SCRIPT_MODULE):
        mapping[".".join(re[0].split(".")[ 1 : ])] = re[1] 
    return mapping

def get_command():
    '''
    Return: dict of commands 
    '''
    mapping = {}
    for mod in load_module(settings.COMMAND_MODEULE):
        for item in dir(mod):
            if item == 'TopCommand':
                continue
            item = getattr(mod, item)
            if isclass(item) and issubclass(item, TopCommand):
                mapping[ mod.__name__.split('.')[-1] ] = item()
    return mapping

def load_config(config_file, section):
    '''
    load custom configure by section
    '''
    config = Config(config_file=config_file)
    settings.CONFIG = config
    for re in config.get_config_list(section):
        setattr(settings, re[0].upper(), re[1])

def get_attr(attr_name, default=None):
    '''
    get attribute of startpro.core.settings safety default value
    '''
    if hasattr(settings, attr_name.upper()):
        return getattr(settings, attr_name.upper())
    else:
        return default