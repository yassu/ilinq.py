#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from nose.tools import raises
from ilinq.ilinq import Linq
from ilinq.igroup import IPair, IGroup


class TestLinq(unittest.TestCase):

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

    def test_take2(self):
        linq = Linq([1, 2])
        self.assertEqual(linq.take(5).to_list(), [1, 2])

    def test_concat(self):
        linq1 = Linq([1, 2])
        linq2 = Linq([3, 4])
        self.assertEqual(linq1.concat(linq2), Linq([1, 2, 3, 4]))
        self.assertEqual(linq1, Linq([1, 2]))
        self.assertEqual(linq2, Linq([3, 4]))

    def test_concat2(self):
        linq1 = Linq([1, 2])
        linq2 = Linq([3, 4])
        linq3 = Linq([5, 6])
        self.assertEqual(linq1.concat(linq2, linq3), Linq([1, 2, 3, 4, 5, 6]))
        self.assertEqual(linq1, Linq([1, 2]))
        self.assertEqual(linq2, Linq([3, 4]))

    def test_distinct(self):
        linq = Linq([-1, 1, 1, 2, 3, -1, 2, 1])
        self.assertEqual(linq.distinct().to_list(), [-1, 1, 2, 3])

    def test_order_by(self):
        items = [
            {'x': 1, 'y': 2},
            {'x': 3, 'y': 4},
            {'x': 1, 'y': 1}
        ]
        linq = Linq(items)
        self.assertEqual(
            linq
            .order_by(func=lambda obj: (obj['x'], obj['y']))
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
            .order_by(func=lambda obj: (obj['x'], obj['y']), desc=True)
            .to_list(),
            [{'x': 3, 'y': 4}, {'x': 1, 'y': 2}, {'x': 1, 'y': 1}]
        )

    def test_inject(self):
        linq = Linq([1, 2, 3, 4])
        # 0 - 1 - 2 - 3 - 4
        self.assertEqual(linq.inject(0, lambda res, val: res - val), -10)
        self.assertEqual(linq.inject(0, lambda res, val: res - val), -10)

    def test_count(self):
        self.assertEqual(Linq([2, 4, 6, 8, 10]).count(), 5)

    def test_count2(self):
        self.assertEqual(Linq([2, 4, 6, 8, 10]).count(lambda n: n > 5), 3)

    def test_single(self):
        linq = Linq([1])
        self.assertEqual(linq.single(), 1)
        self.assertEqual(linq.single(), 1)

    @raises(IndexError)
    def test_single2(self):
        linq = Linq([])
        linq.single()

    @raises(IndexError)
    def test_single3(self):
        linq = Linq([1, 2])
        linq.single()

    def test_single_or_default(self):
        linq = Linq([1])
        self.assertEqual(linq.single_or_default(), 1)

    def test_single_or_default2(self):
        linq = Linq(tuple())
        self.assertEqual(linq.single_or_default(default=10), 10)

    @raises(IndexError)
    def test_single_or_default3(self):
        linq = Linq(tuple([1, 2]))
        linq.single_or_default(default=10)

    def test_first(self):
        linq = Linq([11, 13, 15, 19])
        self.assertEqual(linq.first(), 11)
        self.assertEqual(linq.first(), 11)

    @raises(IndexError)
    def test_first2(self):
        linq = Linq([])
        linq.first()

    def test_first3(self):
        linq = Linq([11, 14, 15, 19])
        self.assertEqual(linq.first(func=lambda x: x % 2 == 0), 14)
        self.assertEqual(linq.first(func=lambda x: x % 2 == 0), 14)

    def test_first_or_default(self):
        linq = Linq([11, 13, 15, 19])
        self.assertEqual(linq.first_or_default(), 11)
        self.assertEqual(linq.first_or_default(), 11)

    def test_first_or_default2(self):
        linq = Linq([])
        self.assertEqual(linq.first_or_default(), None)
        self.assertEqual(linq.first_or_default(default=100), 100)
        self.assertEqual(linq.first_or_default(default=100), 100)

    def test_first_or_default3(self):
        linq = Linq([11, 14, 15, 19])
        self.assertEqual(linq.first_or_default(func=lambda x: x % 2 == 0), 14)
        self.assertEqual(linq.first_or_default(func=lambda x: x % 2 == 0), 14)

    def test_last(self):
        linq = Linq([11, 13, 15, 19])
        self.assertEqual(linq.last(), 19)
        self.assertEqual(linq.last(), 19)

    @raises(IndexError)
    def test_last2(self):
        linq = Linq([])
        linq.last()

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

    @raises(IndexError)
    def test_element_at3(self):
        linq = Linq([])
        linq.element_at(2)

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
        self.assertEqual(linq.min(func=lambda x: x % 4), 100)
        self.assertEqual(linq.min(func=lambda x: x % 4), 100)

    @raises(StopIteration)
    def test_min3(self):
        linq = Linq([])
        linq.min()

    def test_max(self):
        linq = Linq([13, 19, 11, 15])
        self.assertEqual(linq.max(), 19)
        self.assertEqual(linq.max(), 19)

    def test_max2(self):
        linq = Linq([1, 6, 1, 4, 2, 2])
        self.assertEqual(linq.max(func=lambda x: x % 2), 1)
        self.assertEqual(linq.max(func=lambda x: x % 2), 1)

    @raises(StopIteration)
    def test_max3(self):
        linq = Linq([])
        linq.max()

    def test_sum(self):
        linq = Linq([1, 1, 4, 2, 2])
        self.assertEqual(linq.sum(), 10)
        self.assertEqual(linq.sum(), 10)

    def test_sum2(self):
        linq = Linq([1, 1, 4, 2, 2])
        self.assertEqual(linq.sum(func=lambda x: x*x), 26)
        self.assertEqual(linq.sum(func=lambda x: x*x), 26)

    def test_sum3(self):
        linq = Linq([])
        self.assertEqual(linq.sum(), 0)

    def test_average(self):
        linq = Linq([1.0, 1.0, 4.0, 2.0, 2.0])
        ave = linq.average()
        self.assertTrue(2 - 0.0002 < ave and ave < 2 + 0.0002)

    def test_average2(self):
        linq = Linq([1.0, 1.0, 4.0, 2.0, 2.0])
        ave = linq.average(func=lambda x: x*x)
        self.assertTrue(5.2 - 0.0002 < ave and ave < 5.2 + 0.0002)

    @raises(ZeroDivisionError)
    def test_average3(self):
        linq = Linq([])
        linq.average()

    def test_contain(self):
        linq = Linq([1, 6, 1, 4, 2, 2])
        self.assertTrue(linq.contains(2))
        self.assertTrue(linq.contains(2))

    def test_contain2(self):
        linq = Linq([1, 6, 1, 4, 2, 2])
        self.assertFalse(linq.contains(100))
        self.assertFalse(linq.contains(100))

    def test_contain3(self):
        linq = Linq([1, 2, 3])
        self.assertTrue(linq.contains(101, func=lambda n: n % 100))
        self.assertFalse(linq.contains(100, func=lambda n: n % 100))

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
        self.assertTrue(linq.any(func=lambda x: x % 2 == 0))
        self.assertTrue(linq.any(func=lambda x: x % 2 == 0))

    def test_any4(self):
        linq = Linq([2, 3, 4, 5])
        self.assertFalse(linq.any(func=lambda x: x > 10))
        self.assertFalse(linq.any(func=lambda x: x > 10))

    def test_group_by(self):
        linq = Linq([1, 2, 3, 4, 5])
        self.assertEqual(
            linq.group_by(lambda n: n % 2),
            IGroup([
                IPair(1, [1, 3, 5]),
                IPair(0, [2, 4])
            ]))

    def test_to_list(self):
        self.assertEqual(Linq([1]).to_list(), [1])
        self.assertEqual(Linq([1, 1, 2, 3, 5]).to_list(), [1, 1, 2, 3, 5])

    def test_str0(self):
        self.assertEqual(str(Linq([])), 'Linq<>')

    def test_str1(self):
        self.assertEqual(str(Linq([1])), 'Linq<1>')

    def test_str2(self):
        self.assertEqual(str(Linq([1, 2])), 'Linq<1, 2>')

    def test_repr0(self):
        self.assertEqual(repr(Linq([])), 'Linq<>')

    def test_repr1(self):
        self.assertEqual(repr(Linq([1])), 'Linq<1>')

    def test_repr2(self):
        self.assertEqual(repr(Linq([1, 2])), 'Linq<1, 2>')
