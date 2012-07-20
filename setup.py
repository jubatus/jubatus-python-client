try:
    from setuptools import setup
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
      version="0.3.1",
      description="client for jubatus: highly distributed online machine learning system",
      long_description=read('README.rst'),
      author='PFI & NTT',
      author_email='',
      url='http://jubat.us',
      license='LGPL',
      platforms='Linux',
      packages=['jubatus'],
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
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Information Analysis'
      ],

      test_suite='it_single_test.suite',
)
