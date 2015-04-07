# Startpro

Use **startpro** script to build a Python script project quickly.

### Getting Started

```shell
pip install startpro
```

> raise pkg_resources.DistributionNotFound? ( https://github.com/Homebrew/homebrew/issues/26900 )

### Usage

```shell
startpro command [-options] [option_value]

Available command:
  create
  list
  pkg
  start
```

#### New Features*

```shell
from startpro.common.utils.log4py import log
from startpro.core.utils.loader import safe_init_run
from startpro.core.utils.loader import get_settings

@safe_init_run
def run(**kw):
	pass

```
1. Add safe init run model
2. Add log config for mail service in config.ini (safe_init_run model only),if the log error logging more than 50, it will be sent to your e-mail.
```shell
[common]
mail_to = 
mail_un = 
mail_pw = 
mail_host = 

# custom config
# [test]
# lol = LOL
```


#### Help

```shell
startpro [command] -help
```

#### Build a project

```shell
startpro cretae -name pro
```

#### Settings

```shell
cd pro

vim startpro.cfg

# [settings]
# default = 'execute module match pattern name'
# [package]
# name = 'package main process name'

```

#### Example
```shell
➜ startpro create -name pro
➜ cd pro
➜ mkdir script
➜ touch script/__init__.py
➜ vim script/test.py
➜ startpro list
  [INFO]:script list:
  ----> test.run
➜ startpro start test.run
  {'paths': ['script'], 'load_paths': ['script.test']}

```

test.py (function)

function name startswith "run":

```python
def run(**k):
	print k
```
or

class extends Process & has attribute "name"
and overwrite:
```python
def run(self, **kwargvs):
        raise NotImplementedError
```

test.py (class)

```python
# encoding: utf8
from startpro.core.process import Process

class Test(Process):

	name = "testpro"

	def __init__(self):
		pass

	def run(self, **k):
		print k
```

#### Start a program
```shell
➜ startpro list
  [INFO]:script list:
  ----> testpro
➜ startpro start testpro
...
```

#### Package
```shell
➜ startpro pkg -name pro
➜ ./dist/pro list
  [INFO]:script list:
  ----> testpro
➜ ./dist/pro start testpro

```

#### Thanks
Thanks to ChengZhang <https://github.com/sing1ee> and @LL




