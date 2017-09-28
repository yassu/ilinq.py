#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ilinq.ilookup import ILookup
from ilinq.ilinq import Linq
from nose.tools import assert_equal


class Test_ILookup(object):
    def init_test(self):
        ILookup()

    def init_test2(self):
        ILookup([[1, 2], [3, 4]])

    def to_linq_test(self):
        assert_equal(
            ILookup({1: 2, 2: 3, 3: 6}).to_linq(),
            Linq([(1, 2), (2, 3), (3, 6)]))
