# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import deep_learning

setup(
 
  name='deep_learning',
 
  version='1.0.0',
 
  packages=find_packages(exclude=["docs", "examples", "tests"]),
 
  author="Benjamin & Kevin",

  description="Deep learning package",

  long_description=open('README.md').read(),
 
  #Enables MANIFEST.in to be taken account
  include_package_data=True,

  classifiers=[
    "Programming Language :: Python",
    "Development Status :: 1 - Planning",
    "License :: MIT",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.7",
    "Topic :: Deep learning",
  ],
 
  install_requires=[
    'bs4',
    'six',
    'lxml',
    'requests',
    'numpy',
    'coloredlogs',
    'tensorflow',
    'scipy',
    'scikit-learn',
    'pillow==2.9.0',
    'keras',
    'imutils',
    'h5py'
  ],

  setup_requires=['pytest-runner'],

  tests_require=['pytest'],
  license="MIT",
)
