#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='ilinq',
      version='0.0.1',
      description='linq library',
      author='yassu',
      author_email='yasu0320.dev@gmail.com',
      url='https://github.com/yassu/Ilinq.py',
      extra_require={'dev': open('extra_require.txt').read().split('\n')}
      )
