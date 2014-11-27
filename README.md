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



