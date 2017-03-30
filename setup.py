import os

from setuptools import find_packages

with open(os.path.join(os.path.dirname(__file__), 'startpro/VERSION')) as f:
    version = f.read().strip()

scripts = ['bin/startpro']
if os.name == 'nt':
    scripts.append('bin/startpro.bat')

setup_args = {
    'name': 'startpro',
    'version': version,
    'url': 'https://github.com/zoe0316/startpro',
    'description': 'build a script project',
    'long_description': open('README.rst').read(),
    'author': 'Zoe Allen',
    'author_email': 'zoe0316@live.cn',
    'maintainer': '',
    'maintainer_email': '',
    'scripts': scripts,
    'license': 'BSD',
    'include_package_data': True,
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: BSD License',

        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',

        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
else:
    setup_args['install_requires'] = [
        'pyinstaller',
    ]

setup(
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test", "script"]),
    **setup_args
)
