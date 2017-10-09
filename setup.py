#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from ilinq import __VERSION__

classifiers = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
]

setup(
    name='ilinq',
    version=__VERSION__,
    description='linq library',
    long_description=open('Readme.rst').read(),
    author='yassu',
    author_email='yasu0320.dev@gmail.com',
    classifiers=classifiers,
    packages=find_packages(),
    url='https://github.com/yassu/ilinq.py',
  )
