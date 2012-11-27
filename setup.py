try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import os
import sys
import unittest
import os.path
import platform

sys.path.append('jubatus')
sys.path.append('test')

def read(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()

setup(name='jubatus',
      version=read('VERSION').rstrip(),
      description='Jubatus is a distributed processing framework and streaming machine learning library. This is the Jubatus client in Python.',
      long_description=read('README.rst'),
      author='PFI & NTT',
      author_email='jubatus@googlegroups.com',
      url='http://jubat.us',
      download_url='http://pypi.python.org/pypi/jubatus/',
      license='MIT License',
      platforms='Linux',
      packages=find_packages(exclude=['test']),
      install_requires=[
          'msgpack-rpc-python>=0.3.0'
      ],

      entry_points="",
      ext_modules=[],
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Other Environment',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Information Analysis'
      ],

      test_suite='jubatus_test',
)
