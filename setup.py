try:
    import concurrent
except ImportError:
    pass

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

def get_install_requires():
    if sys.version_info < (2, 7):
        install_requires = [
            'tornado<=4.4.3',
            'msgpack-rpc-python>=0.3.0',
        ]
    else:
        install_requires = [
            'msgpack-rpc-python>=0.3.0',
        ]
    return install_requires
        

setup(name='jubatus',
      version=read('VERSION').rstrip(),
      description='Jubatus is a distributed processing framework and streaming machine learning library. This is the Jubatus client in Python.',
      long_description=read('README.rst'),
      author='PFN & NTT',
      author_email='jubatus-team@googlegroups.com',
      url='http://jubat.us',
      download_url='http://pypi.python.org/pypi/jubatus/',
      license='MIT License',
      platforms='Linux',
      packages=find_packages(exclude=['test']),
      install_requires=get_install_requires(),

      entry_points="",
      ext_modules=[],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Scientific/Engineering :: Information Analysis'
      ],

      test_suite='jubatus_test.suite',
)
