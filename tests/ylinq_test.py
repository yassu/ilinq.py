#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest
from copy import deepcopy
sys.path.append('./../src/')
from ylinq import Linq


class TestLinq(unittest.TestCase):

    def setUp(self):
        self.linq1 = Linq([1])
        self.linq2 = Linq([1, 1, 2, 3, 5])

    def test_next(self):
        linq1 = deepcopy(self.linq1)
        assert(next(linq1) == 1)

    def test_where(self):
        linq1 = Linq([1])
        linq2 = Linq([1, 1, 2, 3, 5])
        self.assertEqual(linq1.where(lambda x: x % 2 == 1).to_list(), [1])
        self.assertEqual(linq2.where(lambda x: x % 2 == 0).to_list(), [2])

    def test_select(self):
        i = iter(range(5))
        linq = Linq(i)
        self.assertEqual(
            linq.select(lambda x: x % 2 == 0).to_list(),
            [True, False, True, False, True])

    def test_to_list(self):
        self.assertEqual(self.linq1.to_list(), [1])
        self.assertEqual(self.linq2.to_list(), [1, 1, 2, 3, 5])
