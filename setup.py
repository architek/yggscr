import os
import re
import codecs
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='yggscr',
      version=find_version("yggscr", "__init__.py"),
      description='yggscr',
      long_description='Yggscr',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
      ],
      keywords='ygg',
      url='http://meh',
      author='Himself',
      author_email='root@localhost',
      license='MIT',
      packages=['yggscr'],
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires=[
          'robobrowser>=0.5.3',
          'cmd2>=0.8.0',
          'requests[socks]>=2.18.4',
          'cfscrape>=1.9.4',
          'bottle>=0.12.13',
          'transmissionrpc==0.11',
      ],
      scripts=['bin/yshell', 'yserver/yserver'],
      include_package_data=True,
      zip_safe=False)
