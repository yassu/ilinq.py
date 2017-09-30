#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides grouped objects.
"""

from ilinq.ilinq import Linq


class IPair(object):
    """
    This object shows pair of key and value which ``Linq`` instance.
    """
    def __init__(self, key, value_linq):
        if not isinstance(value_linq, Linq):
            raise ValueError('{} is not a linq instance.'.format(value_linq))
        self._key = key
        self._value_linq = value_linq

    @property
    def key(self):
        """
        return key object
        """
        return self._key

    @property
    def values(self):
        """
        return value object
        """
        return self._value_linq

    def __str__(self):
        return '{%s: %s}' % (self.key, self.values)

    def __repr__(self):
        return 'IPair{%s: %s}' % (self.key, self.values)

    def __eq__(self, other):
        return self.key == other.key and self.values == other.values


class IGroup(Linq):
    """
    This object shows the list of ``IPair``.
    This object is used for
    `ilinq.Linq.group_by <ilinq.html#ilinq.ilinq.Linq.group_by>`_.
    """
    def __init__(self, pairs=None):
        if pairs is None:
            pairs = list()

        for pair in pairs:
            if not isinstance(pair, IPair):
                raise ValueError('{} is not a IPair instance.')

        keys = list(map(lambda x: x.key, pairs))
        if len(keys) != len(set(keys)):
            raise ValueError('{} has overlap.')

        super().__init__(pairs)

    @property
    def keys(self):
        """
        return all key objects.
        """
        return [pair.key for pair in self]

    @property
    def values(self):
        """
        return all value objects.
        """
        return [pair.values for pair in self]
