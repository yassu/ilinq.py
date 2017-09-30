#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides ``lookup`` objects.
"""

from ilinq.ilinq import Linq


class ILookup(dict):
    """
    Simple object class which be able to convert to a ``Linq`` object.
    """
    def to_linq(self):
        """
        return ``Linq`` instance which consisted by elements of (key, value).
        """
        return Linq([(key, val) for key, val in self.items()])

    def __str__(self):
        s = '{}<'.format(self.__class__.__name__)
        for key, val in self.items():
            s += '{}: {}'.format(key, val)
            s += ', '
        if len(self) > 0:
            s = s[:-2]
        return s + '>'

    def __repr__(self):
        return str(self)
