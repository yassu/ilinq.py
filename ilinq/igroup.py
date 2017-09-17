#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides grouped objects.
"""

from ilinq.ilinq import Linq


class IPair(object):
    def __init__(self, key, value_linq):
        if not isinstance(value_linq, Linq):
            raise ValueError('{} is not a linq instance.'.format(value_linq))
        self._key = key
        self._value_linq = value_linq

    @property
    def key(self):
        return self._key

    @property
    def values(self):
        return self._value_linq

    def __str__(self):
        return '{%s: %s}' % (self.key, self.values)

    def __repr__(self):
        return 'IPair{%s: %s}' % (self.key, self.values)

    def __eq__(self, other):
        return self.key == other.key and self.values == other.values


class IGroup(Linq):
    @property
    def keys(self):
        return [pair.key for pair in self]

    @property
    def values(self):
        return [pair.values for pair in self]
