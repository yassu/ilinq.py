#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest
from nose.tools import raises
from copy import deepcopy
sys.path.append('./../src/')
from ylinq import Linq


class TestLinq(unittest.TestCase):

    def setUp(self):
        self.linq1 = Linq([1])
        self.linq2 = Linq([1, 1, 2, 3, 5])

    def test_next(self):
        linq1 = deepcopy(self.linq1)
        self.assertEqual(next(linq1), 1)

        linq2 = deepcopy(self.linq2)
        self.assertEqual(next(linq2), 1)
        self.assertEqual(next(linq2), 1)
        self.assertEqual(next(linq2), 2)
        self.assertEqual(next(linq2), 3)
        self.assertEqual(next(linq2), 5)

    def test_where(self):
        linq1 = Linq([1])
        linq2 = Linq([1, 1, 2, 3, 5])
        self.assertEqual(linq1.where(lambda x: x % 2 == 1).to_list(), [1])
        self.assertEqual(linq2.where(lambda x: x % 2 == 0).to_list(), [2])

    def test_select(self):
        linq = Linq(range(5))
        self.assertEqual(
            linq.select(lambda x: x % 2 == 0).to_list(),
            [True, False, True, False, True])

    def test_take(self):
        linq = Linq(range(100))
        self.assertEqual(linq.take(5).to_list(), [0, 1, 2, 3, 4])

    def test_distinct(self):
        linq = Linq([-1, 1, 1, 2, 3, -1, 2, 1])
        self.assertEqual(linq.distinct().to_list(), [-1, 1, 2, 3])

    def test_take2(self):
        linq = Linq([1, 2])
        self.assertEqual(linq.take(5).to_list(), [1, 2])

    def test_order_by(self):
        items = [
            {'x': 1, 'y': 2},
            {'x': 3, 'y': 4},
            {'x': 1, 'y': 1}
        ]
        linq = Linq(items)
        self.assertEqual(
            linq
            .order_by(lambda obj: (obj['x'], obj['y']))
            .to_list(),
            [{'x': 1, 'y': 1}, {'x': 1, 'y': 2}, {'x': 3, 'y': 4}]
        )

    def test_order_by_desc(self):
        items = [
            {'x': 1, 'y': 2},
            {'x': 3, 'y': 4},
            {'x': 1, 'y': 1}
        ]
        linq = Linq(items)
        self.assertEqual(
            linq
            .order_by(lambda obj: (obj['x'], obj['y']), desc=True)
            .to_list(),
            [{'x': 3, 'y': 4}, {'x': 1, 'y': 2}, {'x': 1, 'y': 1}]
        )

    def test_inject(self):
        linq = Linq([1, 2, 3, 4])
        # 0 - 1 - 2 - 3 - 4
        self.assertEqual(linq.inject(0, lambda res, val: res - val), -10)
        self.assertEqual(linq.inject(0, lambda res, val: res - val), -10)

    def test_count(self):
        self.assertEqual(self.linq2.count(), 5)
        self.assertEqual(self.linq2.count(), 5)

    def test_first(self):
        linq = Linq([11, 13, 15, 19])
        self.assertEqual(linq.first(), 11)
        self.assertEqual(linq.first(), 11)

    def test_first_or_default(self):
        linq = Linq([11, 13, 15, 19])
        self.assertEqual(linq.first_or_default(), 11)
        self.assertEqual(linq.first_or_default(), 11)

    def test_first_or_default2(self):
        linq = Linq([])
        self.assertEqual(linq.first_or_default(), None)
        self.assertEqual(linq.first_or_default(100), 100)

    def test_last(self):
        linq = Linq([11, 13, 15, 19])
        self.assertEqual(linq.last(), 19)
        self.assertEqual(linq.last(), 19)

    def test_last_or_default(self):
        linq = Linq([11, 13, 15, 19])
        self.assertEqual(linq.last_or_default(), 19)
        self.assertEqual(linq.last_or_default(), 19)

    def test_last_or_default2(self):
        linq = Linq([])
        self.assertEqual(linq.last_or_default(), None)
        self.assertEqual(linq.last_or_default(default=10), 10)

    def test_element_at(self):
        linq = Linq([11, 13, 15, 19])
        self.assertEqual(linq.element_at(2), 15)
        self.assertEqual(linq.element_at(2), 15)

    @raises(IndexError)
    def test_element_at2(self):
        linq = Linq([11])
        linq.element_at(3)

    def test_element_at_or_default(self):
        linq = Linq([11, 13, 15, 19])
        self.assertEqual(linq.element_at_or_default(2), 15)
        self.assertEqual(linq.element_at_or_default(2), 15)

    def test_element_at_or_default2(self):
        linq = Linq([11])
        self.assertEqual(linq.element_at_or_default(2), None)
        self.assertEqual(linq.element_at_or_default(2, default=3), 3)

    def test_min(self):
        linq = Linq([13, 19, 11, 15])
        self.assertEqual(linq.min(), 11)
        self.assertEqual(linq.min(), 11)

    def test_min2(self):
        linq = Linq([13, 18, 11, 100])
        self.assertEqual(linq.min(key=lambda x: x % 4), 100)
        self.assertEqual(linq.min(key=lambda x: x % 4), 100)

    def test_max(self):
        linq = Linq([13, 19, 11, 15])
        self.assertEqual(linq.max(), 19)
        self.assertEqual(linq.max(), 19)

    def test_max2(self):
        linq = Linq([1, 6, 1, 4, 2, 2])
        self.assertEqual(linq.max(key=lambda x: x % 2), 1)
        self.assertEqual(linq.max(key=lambda x: x % 2), 1)

    def test_sum(self):
        linq = Linq([1, 1, 4, 2, 2])
        self.assertEqual(linq.sum(), 10)
        self.assertEqual(linq.sum(), 10)

    def test_sum2(self):
        linq = Linq([1, 1, 4, 2, 2])
        self.assertEqual(linq.sum(func=lambda x: x*x), 26)
        self.assertEqual(linq.sum(func=lambda x: x*x), 26)

    def test_average(self):
        linq = Linq([1.0, 1.0, 4.0, 2.0, 2.0])
        ave = linq.average()
        self.assertTrue(2 - 0.0002 < ave and ave < 2 + 0.0002)

    def test_average2(self):
        linq = Linq([1.0, 1.0, 4.0, 2.0, 2.0])
        ave = linq.average(func=lambda x: x*x)
        self.assertTrue(5.2 - 0.0002 < ave and ave < 5.2 + 0.0002)

    def test_contain(self):
        linq = Linq([1, 6, 1, 4, 2, 2])
        self.assertTrue(linq.contains(2))
        self.assertTrue(linq.contains(2))

    def test_contain2(self):
        linq = Linq([1, 6, 1, 4, 2, 2])
        self.assertFalse(linq.contains(100))
        self.assertFalse(linq.contains(100))

    def test_all(self):
        linq = Linq([1, 1, 3, 4, 5, 7, 9, 11])
        self.assertFalse(linq.all(lambda x: x % 2 == 1))
        self.assertFalse(linq.all(lambda x: x % 2 == 1))

    def test_all2(self):
        linq = Linq([1, 1, 3, 5, 7, 9, 11])
        self.assertTrue(linq.all(lambda x: x % 2 == 1))
        self.assertTrue(linq.all(lambda x: x % 2 == 1))

    def test_any(self):
        linq = Linq([])
        self.assertFalse(linq.any())
        self.assertFalse(linq.any())

    def test_any2(self):
        linq = Linq([1])
        self.assertTrue(linq.any())
        self.assertTrue(linq.any())

    def test_any3(self):
        linq = Linq([2, 3, 4, 5])
        self.assertTrue(linq.any(lambda x: x % 2 == 0))
        self.assertTrue(linq.any(lambda x: x % 2 == 0))

    def test_any4(self):
        linq = Linq([2, 3, 4, 5])
        self.assertFalse(linq.any(lambda x: x > 10))
        self.assertFalse(linq.any(lambda x: x > 10))

    def test_to_list(self):
        self.assertEqual(self.linq1.to_list(), [1])
        self.assertEqual(self.linq2.to_list(), [1, 1, 2, 3, 5])
