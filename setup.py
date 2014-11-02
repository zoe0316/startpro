from setuptools import setup, find_packages
from distutils.command.install_data import install_data
import os
import sys

class osx_install_data(install_data):
    
    def finalize_options(self):
        self.set_undefined_options('install', ('install_lib', 'install_dir'))
        install_data.finalize_options(self)

if sys.platform == "darwin":
    cmdclasses = {'install_data': osx_install_data}
else:
    cmdclasses = {'install_data': install_data}

with open(os.path.join(os.path.dirname(__file__), 'startpro/VERSION')) as f:
    version = f.read().strip()

scripts = ['bin/startpro']
if os.name == 'nt':
    scripts.append('bin/startpro.bat')

setup_args = {
    'name': 'Startpro',
    'version': version,
    'url': 'http://zoe0316.github.io',
    'description': 'build a script project',
    'long_description': open('README.md').read(),
    'author': 'Zoe Allen',
    'maintainer': '',
    'maintainer_email': '',
    # 'cmdclass': cmdclasses,
    'scripts': scripts,
    'license': 'BSD',
    'include_package_data': True,
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
}

setup(
    packages = find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
#     entry_points = {
#         'console_scripts': [
#             'startpro = startpro:run',
#         ],
#     },
    exclude_package_data = { '': ['README.txt'] },
    **setup_args
)