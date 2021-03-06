#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
import sys
import datetime
from distutils.version import StrictVersion

try:
    from setuptools import setup, __version__, find_packages
except ImportError:
    sys.exit('You need to install python3 setuptools')

if sys.version_info < (3, 4):
    sys.exit('Sorry, Python < 3.4 is not supported')
if StrictVersion(__version__) < StrictVersion('33.1.1'):
    sys.exit('Sorry, Python3 setuptools < 33.1.1 is not supported')

with open('src/yggscr/__build__.py', 'w') as f:
    builddate = format(datetime.datetime.now())[:19]
    f.write("__builddate__ = '{}'".format(builddate))

setup(name='yggscr',
      version='1.2.18',
      description='Yggtorrent scraper library - Webserver - Rss - Shell',
      keywords='yggscr',
      author='Laurent Kislaire',
      author_email='teebeenator@gmail.com',
      url='https://github.com/architek/yggscr',
      license='ISC',
      long_description=io.open(
          './docs/README.rst', 'r', encoding='utf-8').read(),
      platforms='any',
      python_requires='>= 3.4',
      zip_safe=False,
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Programming Language :: Python :: 3 :: Only',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
                   ],
      packages=find_packages('src', exclude=('tests',)),
      package_dir={'': 'src'},
      include_package_data=False,
      install_requires=[
          'robobrowser>=0.5.3',
          'cmd2>=0.8.0',
          'requests[socks]>=2.18.4',
          'cfscrape>=1.9.6',
          'bottle>=0.12.13',
          'bottle-werkzeug>=0.1.1',
          'transmissionrpc>=0.11',
          'deluge_client>=1.6.0',
          'configparser>=3.5.0',
      ],
      tests_require=[
          "pytest>=3.6.0",
          "mock",
          "pytest-timeout",
      ],
      test_suite="tests",
      entry_points={
          'console_scripts': [
              'yshell = yggscr.__main__:main',
              'yshout = yggscr.shout:main',
              'yserver = yserver.__main__:main',
          ]
      },
      )
