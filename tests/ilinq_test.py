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
        self.assertEqual(linq1.where(lambda x: x % 2 == 1), Linq([1]))
        self.assertEqual(linq2.where(lambda x: x % 2 == 0), Linq([2]))

    def test_where2(self):
        linq1 = Linq([1])
        linq2 = Linq([1, 1, 2, 3, 5])
        self.assertEqual(linq1.where(), Linq([1]))
        self.assertEqual(linq2.where(), Linq([1, 1, 2, 3, 5]))

    def test_where_in(self):
        self.assertEqual(
            Linq(range(10)).where_in((1, 3, 7, 9, 13, 15)),
            Linq([1, 3, 7, 9]))

    def test_where_in2(self):
        self.assertEqual(
            Linq(range(10)).where_in(
                (1, 3, 7, 9, 13, 15),
                select_f=lambda x: x % 5),
            Linq([1, 3, 6, 8]))

    def test_select(self):
        linq = Linq(range(5))
        self.assertEqual(
            linq.select(lambda x: x % 2 == 0),
            Linq([True, False, True, False, True]))

    def test_select2(self):
        linq = Linq(range(5))
        self.assertEqual(
            linq.select(),
            Linq(range(5)))

    def test_select_i(self):
        linq = Linq(range(5))
        self.assertEqual(
            linq.select_i(),
            Linq(range(5))
        )

    def test_select_i2(self):
        linq = Linq(range(5)).reverse()
        self.assertEqual(
            linq.select_i(lambda i, x: x ** i),
            Linq([4**0, 3**1, 2**2, 1**3, 0**4])
        )

    def test_select_many(self):
        linq = Linq(
            [
                {"ids": [0, 1, 2, 3, 4, 5]},
                {"ids": [6, 7, 8, 9]}
            ]
        )
        self.assertEqual(
            linq.select_many(lambda x: x["ids"]),
            list(range(10)))

    def test_select_many2(self):
        linq = Linq(
            [
                [0, 1, 2, 3, 4, 5],
                [6, 7, 8, 9]
            ]
        )
        self.assertEqual(
            linq.select_many(),
            Linq(range(10)))

    def test_select_many_i(self):
        linq = Linq(
            [
                [0, 1, 2, 3, 4, 5],
                [6, 7, 8, 9]
            ]
        )
        self.assertEqual(
            linq.select_many_i(),
            Linq(range(10))
        )

    def test_select_many_i2(self):
        linq = Linq(
            [
                [9, 8, 7, 6],
                [5, 4, 3, 2, 1, 0]
            ]
        )
        self.assertEqual(
            linq.select_many_i(lambda i, x: i ** x),
            Linq(
                [0 ** 9, 1**8, 2**7, 3**6, 4**5, 5**4, 6**3, 7**2, 8**1, 9**0])
        )

    def test_take(self):
        linq = Linq(range(100))
        self.assertEqual(linq.take(5), Linq([0, 1, 2, 3, 4]))

    def test_take2(self):
        linq = Linq([1, 2])
        self.assertEqual(linq.take(5), Linq([1, 2]))

    def test_take_while(self):
        self.assertEqual(
            Linq(range(10)).take_while(lambda x: x < 5),
            Linq(range(5)))

    def test_take_while2(self):
        self.assertEqual(
            Linq(range(10)).take_while(lambda x: x < 100),
            Linq(range(10)))

    def test_take_while3(self):
        self.assertEqual(
            Linq(range(10)).take_while(),
            Linq(range(10)))

    def test_take_while_i(self):
        linq = Linq(range(10)).concat(Linq(range(10)).reverse())
        self.assertEqual(
            linq.take_while_i(lambda i, x: i * x <= 10),
            Linq(range(4))
        )

    def test_take_while_i2(self):
        linq = Linq(range(10)).concat(Linq(range(10)).reverse())
        self.assertEqual(
            linq.take_while_i(),
            Linq(range(10)).concat(Linq(range(10)).reverse())
        )

    def test_skip(self):
        self.assertEqual(
            Linq(range(10)).reverse().skip(3),
            Linq([6, 5, 4, 3, 2, 1, 0]))

    def test_skip2(self):
        self.assertEqual(
            Linq([3, 2, 1]).skip(3),
            Linq([])
        )

    @raises(IndexError)
    def test_skip3(self):
        Linq(range(2)).skip(5)

    def test_skip_while(self):
        self.assertEqual(
            Linq([5, 4, 3, 100, 2, 101, 1, 102]).skip_while(),
            Linq([5, 4, 3, 100, 2, 101, 1, 102]))

    def test_skip_while2(self):
        self.assertEqual(
            Linq([5, 4, 3, 100, 2, 101, 1, 102]).skip_while(
                lambda x: x < 50),
            Linq([100, 2, 101, 1, 102]))

    def test_skip_while_i(self):
        self.assertEqual(
            Linq(range(10)).skip_while_i(),
            Linq(range(10))
        )

    def test_skip_while_i2(self):
        self.assertEqual(
            Linq(range(10)).skip_while_i(lambda i, x: i * x < 10),
            Linq([4, 5, 6, 7, 8, 9])
        )

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

    def test_default_if_empty(self):
        linq = Linq([1, 2])
        self.assertEqual(linq.default_if_empty(), Linq([1, 2]))

    def test_default_if_empty2(self):
        linq = Linq([])
        self.assertEqual(linq.default_if_empty(), Linq([None]))
        self.assertEqual(linq.default_if_empty(default=3), Linq([3]))

    def test_distinct(self):
        linq = Linq([-1, 1, 1, 2, 3, -1, 2, 1])
        self.assertEqual(linq.distinct(), Linq([-1, 1, 2, 3]))

    def test_distinct2(self):
        linq = Linq([-1, 2, 1, 2, 3, -1, 2, 1])
        self.assertEqual(linq.distinct(lambda x: x*x), Linq([-1, 2, 3]))

    def test_except(self):
        linq1 = Linq([2.0, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5])
        linq2 = Linq([2.1, 2.2])
        self.assertEqual(linq1.except_(linq2), Linq([2.0, 2.0, 2.3, 2.4, 2.5]))

    def test_except2(self):
        linq1 = Linq([2.0, -2.0, 2.1, -2.2, 2.3, 2.4, 2.5, 2.3])
        linq2 = Linq([2.1, 2.2])
        self.assertEqual(linq1.except_(
                linq2, key_f=lambda x: abs(x)),
            Linq([2.0, -2.0, 2.3, 2.4, 2.5, 2.3]))

    def test_intersect(self):
        linq1 = Linq([2.0, -2.0, 2.1, -2.2, 2.3, 2.4, 2.5, 2.3])
        linq2 = Linq([2.1, 2.2])
        self.assertEqual(linq1.intersect(
                linq2),
            Linq([2.1]))

    def test_union(self):
        linq = Linq('abcdef').union('xyz')
        self.assertEqual(
            linq,
            Linq('abcdefxyz'))
        self.assertTrue(isinstance(linq, Linq))

    def test_union2(self):
        linq = Linq('abcdef').union('defdefxyz')
        self.assertEqual(
            linq,
            Linq('abcdefxyz'))
        self.assertTrue(isinstance(linq, Linq))

    def test_zip(self):
        self.assertEqual(
            Linq([1, 2, 3]).zip([4, 5, 6], lambda x, y: x + y),
            Linq([1 + 4, 2 + 5, 3 + 6]))

    def test_zip2(self):
        self.assertEqual(
            Linq([1, 2]).zip([4, 5, 6], lambda x, y: x - y),
            Linq([1 - 4, 2 - 5]))

    def test_zip3(self):
        self.assertEqual(
            Linq([1, 2, 3]).zip([4, 5], lambda x, y: x + y),
            Linq([1 + 4, 2 + 5]))

    def test_repeat(self):
        self.assertEqual(Linq.repeat(1, 3), Linq([1, 1, 1]))

    def test_reverse(self):
        linq = Linq(range(6)).reverse()
        self.assertEqual(linq, Linq([5, 4, 3, 2, 1, 0]))
        self.assertTrue(isinstance(linq, Linq))

    def test_order_by(self):
        items = [
            {'x': 1, 'y': 2},
            {'x': 3, 'y': 4},
            {'x': 1, 'y': 1}
        ]
        linq = Linq(items)
        self.assertEqual(
            linq
            .order_by(key_f=lambda obj: (obj['x'], obj['y'])),
            Linq([{'x': 1, 'y': 1}, {'x': 1, 'y': 2}, {'x': 3, 'y': 4}])
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
            .order_by(key_f=lambda obj: (obj['x'], obj['y']), desc=True),
            Linq([{'x': 3, 'y': 4}, {'x': 1, 'y': 2}, {'x': 1, 'y': 1}])
        )

    def test_inject(self):
        linq = Linq([1, 2, 3, 4])
        # 0 - 1 - 2 - 3 - 4
        self.assertEqual(linq.inject(0, lambda res, val: res - val), -10)
        self.assertEqual(linq.inject(0, lambda res, val: res - val), -10)

    def test_inject2(self):
        linq = Linq([1, 2, 3, 4])
        # the equare of 0 - 1 - 2 - 3 - 4
        self.assertEqual(
            linq.inject(0, lambda res, val: res - val, last_f=lambda x: x * x),
            100)
        self.assertEqual(
            linq.inject(0, lambda res, val: res - val, last_f=lambda x: x * x),
            100)

    def test_count(self):
        self.assertEqual(Linq([2, 4, 6, 8, 10]).count(), 5)

    def test_count2(self):
        self.assertEqual(
            Linq([2, 4, 6, 8, 10])
            .count(cond_f=lambda n: n > 5),
            3)

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

    def test_single4(self):
        linq = Linq([1, 1, 2, 3, 5])
        self.assertEqual(linq.single(cond_f=lambda x: x % 2 == 0), 2)

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

    def test_single_or_default4(self):
        linq = Linq([1, 2, 3, 4, 5])
        self.assertEqual(
            linq.single_or_default(cond_f=lambda x: x % 3 == 0), 3)

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
        self.assertEqual(linq.first(cond_f=lambda x: x % 2 == 0), 14)
        self.assertEqual(linq.first(cond_f=lambda x: x % 2 == 0), 14)

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
        self.assertEqual(
            linq.first_or_default(cond_f=lambda x: x % 2 == 0),
            14)
        self.assertEqual(
            linq.first_or_default(cond_f=lambda x: x % 2 == 0),
            14)

    def test_last(self):
        linq = Linq([11, 13, 15, 19])
        self.assertEqual(linq.last(), 19)
        self.assertEqual(linq.last(), 19)

    @raises(IndexError)
    def test_last2(self):
        linq = Linq([])
        linq.last()

    def test_last3(self):
        linq = Linq([11, 13, 15, 19])
        self.assertEqual(linq.last(cond_f=lambda x: x % 3 == 2), 11)
        self.assertEqual(linq.last(cond_f=lambda x: x % 3 == 2), 11)

    def test_last_or_default(self):
        linq = Linq([11, 13, 15, 19])
        self.assertEqual(linq.last_or_default(), 19)
        self.assertEqual(linq.last_or_default(), 19)

    def test_last_or_default2(self):
        linq = Linq([])
        self.assertEqual(linq.last_or_default(), None)
        self.assertEqual(linq.last_or_default(default=10), 10)

    def test_last_or_default3(self):
        linq = Linq([11, 13, 15, 19])
        self.assertEqual(linq.last_or_default(
            default=2, cond_f=lambda x: x > 100), 2)
        self.assertEqual(linq.last_or_default(), 19)

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
        self.assertEqual(linq.min(key_f=lambda x: x % 4), 100)
        self.assertEqual(linq.min(key_f=lambda x: x % 4), 100)

    def test_min_all(self):
        linq = Linq(range(5)).concat(Linq(range(4)))
        self.assertEqual(linq.min_all(), [0, 0])

    def test_min_all2(self):
        linq = Linq(range(5)).concat(Linq(range(4)))
        self.assertEqual(
            linq.min_all(key_f=lambda x: x % 4),
            Linq([0, 4, 0]))

    def test_min_all3(self):
        self.assertEqual(Linq().min_all(), Linq())

    def test_max_all(self):
        linq = Linq(range(5)).concat(Linq(range(5)))
        self.assertEqual(linq.max_all(), Linq([4, 4]))

    def test_max_all2(self):
        linq = Linq(range(10)).concat(Linq(range(20)))
        self.assertEqual(
            linq.max_all(key_f=lambda n: n % 5),
            Linq([4, 9, 4, 9, 14, 19]))

    def test_max_all3(self):
        self.assertEqual(Linq().max_all(), Linq())

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
        self.assertEqual(linq.max(key_f=lambda x: x % 2), 1)
        self.assertEqual(linq.max(key_f=lambda x: x % 2), 1)

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
        self.assertEqual(linq.sum(select_f=lambda x: x*x), 26)
        self.assertEqual(linq.sum(select_f=lambda x: x*x), 26)

    def test_sum3(self):
        linq = Linq([])
        self.assertEqual(linq.sum(), 0)

    def test_average(self):
        linq = Linq([1.0, 1.0, 4.0, 2.0, 2.0])
        ave = linq.average()
        self.assertTrue(2 - 0.0002 < ave and ave < 2 + 0.0002)

    def test_average2(self):
        linq = Linq([1.0, 1.0, 4.0, 2.0, 2.0])
        ave = linq.average(select_f=lambda x: x*x)
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
        self.assertTrue(linq.contains(101, key_f=lambda n: n % 100))
        self.assertFalse(linq.contains(100, key_f=lambda n: n % 100))

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
        self.assertTrue(linq.any(cond_f=lambda x: x % 2 == 0))
        self.assertTrue(linq.any(cond_f=lambda x: x % 2 == 0))

    def test_any4(self):
        linq = Linq([2, 3, 4, 5])
        self.assertFalse(linq.any(cond_f=lambda x: x > 10))
        self.assertFalse(linq.any(cond_f=lambda x: x > 10))

    def test_group_by(self):
        linq = Linq(range(6))
        self.assertEqual(
            linq.group_by(lambda n: n % 2),
            IGroup([
                IPair(0, Linq([0, 2, 4])),
                IPair(1, Linq([1, 3, 5]))
            ]))

    def test_to_list(self):
        self.assertEqual(Linq([1]).to_list(), [1])
        self.assertEqual(Linq([1, 1, 2, 3, 5]).to_list(), [1, 1, 2, 3, 5])

    def test_copy(self):
        linq = Linq(range(10))
        linq_copied = linq.copy()
        self.assertTrue(linq is not linq_copied)
        self.assertEqual(linq, linq_copied)

    def test_to_set(self):
        self.assertEqual(Linq([1, 1, 2, 3, 5]).to_set(), {1, 1, 2, 3, 5})

    def test_to_dict(self):
        self.assertEqual(
            Linq(range(4)).to_dict(key_f=lambda x: x, value_f=lambda x: x * x),
            {0: 0, 1: 1, 2: 4, 3: 9}
        )

    def test_to_dict2(self):
        self.assertEqual(
            Linq(range(4)).to_dict(value_f=lambda x: x * x),
            {0: 0, 1: 1, 2: 4, 3: 9}
        )

    def test_to_dict3(self):
        self.assertEqual(
            Linq(range(4)).to_dict(key_f=lambda x: x * x),
            {0: 0, 1: 1, 4: 2, 9: 3}
        )

    @raises(ValueError)
    def test_to_dict4(self):
        Linq(range(4)).to_dict(key_f=lambda _: 1)

    def test_slice(self):
        linq = Linq(range(5))
        self.assertTrue(linq[3] == 3)

    def test_slice2(self):
        linq = Linq()
        self.assertTrue(isinstance(linq[:], Linq))
        self.assertTrue(linq[:] is not linq)

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
