#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides lookup objects.
"""

from ilinq.ilinq import Linq


class ILookup(dict):
    """
    Simple object class which be able to convert to a Linq object.
    """
    def to_linq(self):
        return Linq([(key, val) for key, val in self.items()])
