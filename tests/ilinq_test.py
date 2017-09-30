#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import (
    assert_equal, assert_true, assert_false, raises, assert_is_instance)
from ilinq.ilinq import Linq
from ilinq.igroup import IPair, IGroup
from ilinq.ilookup import ILookup


class TestLinq:

    def test_where(self):
        linq1 = Linq([1])
        linq2 = Linq([1, 1, 2, 3, 5])
        assert_equal(linq1.where(lambda x: x % 2 == 1), Linq([1]))
        assert_equal(linq2.where(lambda x: x % 2 == 0), Linq([2]))

    def test_where2(self):
        linq1 = Linq([1])
        linq2 = Linq([1, 1, 2, 3, 5])
        assert_equal(linq1.where(), Linq([1]))
        assert_equal(linq2.where(), Linq([1, 1, 2, 3, 5]))

    def test_where_in(self):
        assert_equal(
            Linq(range(10)).where_in((1, 3, 7, 9, 13, 15)),
            Linq([1, 3, 7, 9]))

    def test_where_in2(self):
        assert_equal(
            Linq(range(10)).where_in(
                (1, 3, 7, 9, 13, 15),
                select_f=lambda x: x % 5),
            Linq([1, 3, 6, 8]))

    def test_select(self):
        linq = Linq(range(5))
        assert_equal(
            linq.select(lambda x: x % 2 == 0),
            Linq([True, False, True, False, True]))

    def test_select2(self):
        linq = Linq(range(5))
        assert_equal(
            linq.select(),
            Linq(range(5)))

    def test_select_i(self):
        linq = Linq(range(5))
        assert_equal(
            linq.select_i(),
            Linq(range(5))
        )

    def test_select_i2(self):
        linq = Linq(range(5)).reverse()
        assert_equal(
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
        assert_equal(
            linq.select_many(lambda x: x["ids"]),
            list(range(10)))

    def test_select_many2(self):
        linq = Linq(
            [
                [0, 1, 2, 3, 4, 5],
                [6, 7, 8, 9]
            ]
        )
        assert_equal(
            linq.select_many(),
            Linq(range(10)))

    def test_select_many_i(self):
        linq = Linq(
            [
                [0, 1, 2, 3, 4, 5],
                [6, 7, 8, 9]
            ]
        )
        assert_equal(
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
        assert_equal(
            linq.select_many_i(lambda i, x: i ** x),
            Linq(
                [0 ** 9, 1**8, 2**7, 3**6, 4**5, 5**4, 6**3, 7**2, 8**1, 9**0])
        )

    def test_take(self):
        linq = Linq(range(100))
        assert_equal(linq.take(5), Linq([0, 1, 2, 3, 4]))

    def test_take2(self):
        linq = Linq([1, 2])
        assert_equal(linq.take(5), Linq([1, 2]))

    def test_take_while(self):
        assert_equal(
            Linq(range(10)).take_while(lambda x: x < 5),
            Linq(range(5)))

    def test_take_while2(self):
        assert_equal(
            Linq(range(10)).take_while(lambda x: x < 100),
            Linq(range(10)))

    def test_take_while3(self):
        assert_equal(
            Linq(range(10)).take_while(),
            Linq(range(10)))

    def test_take_while_i(self):
        linq = Linq(range(10)).concat(Linq(range(10)).reverse())
        assert_equal(
            linq.take_while_i(lambda i, x: i * x <= 10),
            Linq(range(4))
        )

    def test_take_while_i2(self):
        linq = Linq(range(10)).concat(Linq(range(10)).reverse())
        assert_equal(
            linq.take_while_i(lambda i, x: i * x <= 100),
            linq
        )

    def test_take_while_i3(self):
        linq = Linq(range(10)).concat(Linq(range(10)).reverse())
        assert_equal(
            linq.take_while_i(),
            Linq(range(10)).concat(Linq(range(10)).reverse())
        )

    def test_skip(self):
        assert_equal(
            Linq(range(10)).reverse().skip(3),
            Linq([6, 5, 4, 3, 2, 1, 0]))

    def test_skip2(self):
        assert_equal(
            Linq([3, 2, 1]).skip(3),
            Linq([])
        )

    @raises(IndexError)
    def test_skip3(self):
        Linq(range(2)).skip(5)

    def test_skip_while(self):
        assert_equal(
            Linq([5, 4, 3, 100, 2, 101, 1, 102]).skip_while(),
            Linq([5, 4, 3, 100, 2, 101, 1, 102]))

    def test_skip_while2(self):
        assert_equal(
            Linq([5, 4, 3, 100, 2, 101, 1, 102]).skip_while(
                lambda x: x < 50),
            Linq([100, 2, 101, 1, 102]))

    def test_skip_while_i(self):
        assert_equal(
            Linq(range(10)).skip_while_i(),
            Linq(range(10))
        )

    def test_skip_while_i2(self):
        assert_equal(
            Linq(range(10)).skip_while_i(lambda i, x: i * x < 10),
            Linq([4, 5, 6, 7, 8, 9])
        )

    def test_concat(self):
        linq1 = Linq([1, 2])
        linq2 = Linq([3, 4])
        assert_equal(linq1.concat(linq2), Linq([1, 2, 3, 4]))
        assert_equal(linq1, Linq([1, 2]))
        assert_equal(linq2, Linq([3, 4]))

    def test_concat2(self):
        linq1 = Linq([1, 2])
        linq2 = Linq([3, 4])
        linq3 = Linq([5, 6])
        assert_equal(linq1.concat(linq2, linq3), Linq([1, 2, 3, 4, 5, 6]))
        assert_equal(linq1, Linq([1, 2]))
        assert_equal(linq2, Linq([3, 4]))

    def test_default_if_empty(self):
        linq = Linq([1, 2])
        assert_equal(linq.default_if_empty(), Linq([1, 2]))

    def test_default_if_empty2(self):
        linq = Linq([])
        assert_equal(linq.default_if_empty(), Linq([None]))
        assert_equal(linq.default_if_empty(default=3), Linq([3]))

    def test_distinct(self):
        linq = Linq([-1, 1, 1, 2, 3, -1, 2, 1])
        assert_equal(linq.distinct(), Linq([-1, 1, 2, 3]))

    def test_distinct2(self):
        linq = Linq([-1, 2, 1, 2, 3, -1, 2, 1])
        assert_equal(linq.distinct(lambda x: x*x), Linq([-1, 2, 3]))

    def test_except(self):
        linq1 = Linq([2.0, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5])
        linq2 = Linq([2.1, 2.2])
        assert_equal(linq1.except_(linq2), Linq([2.0, 2.0, 2.3, 2.4, 2.5]))

    def test_except2(self):
        linq1 = Linq([2.0, -2.0, 2.1, -2.2, 2.3, 2.4, 2.5, 2.3])
        linq2 = Linq([2.1, 2.2])
        assert_equal(linq1.except_(
                linq2, key_f=lambda x: abs(x)),
            Linq([2.0, -2.0, 2.3, 2.4, 2.5, 2.3]))

    def test_intersect(self):
        linq1 = Linq([2.0, -2.0, 2.1, -2.2, 2.3, 2.4, 2.5, 2.3, 2.1])
        linq2 = Linq([2.1, 2.2, 2.1])
        assert_equal(linq1.intersect(
                linq2),
            Linq([2.1]))

    def test_intersect2(self):
        linq1 = Linq([2.0, -2.0, -2.1, -2.2, 2.3, 2.4, 2.5, 2.3, -2.1])
        linq2 = Linq([2.1, 2.2, 2.1])
        assert_equal(linq1.intersect(
                linq2, key_f=abs),
            Linq([-2.1, -2.2]))

    def test_union(self):
        linq = Linq('abcdef').union('xyz')
        assert_equal(
            linq,
            Linq('abcdefxyz'))
        assert_is_instance(linq, Linq)

    def test_union2(self):
        linq = Linq('abcdef').union('defdefxyz')
        assert_equal(
            linq,
            Linq('abcdefxyz'))
        assert_is_instance(linq, Linq)

    def test_union3(self):
        linq = Linq('abcabcdef').union('defxyz')
        assert_equal(
            linq,
            Linq('abcdefxyz'))
        assert_is_instance(linq, Linq)

    def test_union4(self):
        assert_equal(
            Linq([1, 2, -3]).union(Linq([3, 4, 5, 4, -2]), key_f=abs),
            Linq([1, 2, -3, 4, 5]))

    def test_zip(self):
        assert_equal(
            Linq([1, 2, 3]).zip([4, 5, 6], zip_f=lambda x, y: x + y),
            Linq([1 + 4, 2 + 5, 3 + 6]))

    def test_zip2(self):
        assert_equal(
            Linq([1, 2]).zip([4, 5, 6], zip_f=lambda x, y: x - y),
            Linq([1 - 4, 2 - 5]))

    def test_zip3(self):
        assert_equal(
            Linq([1, 2, 3]).zip([4, 5], zip_f=lambda x, y: x + y),
            Linq([1 + 4, 2 + 5]))

    def test_zip4(self):
        assert_equal(
            Linq([1, 2, 3]).zip([4, 5, 6]),
            Linq([(1, 4), (2, 5), (3, 6)])
        )

    def test_repeat(self):
        assert_equal(Linq.repeat(1, 3), Linq([1, 1, 1]))

    def test_reverse(self):
        linq = Linq(range(6)).reverse()
        assert_equal(linq, Linq([5, 4, 3, 2, 1, 0]))
        assert_is_instance(linq, Linq)

    def test_order_by(self):
        items = [
            {'x': 1, 'y': 2},
            {'x': 3, 'y': 4},
            {'x': 1, 'y': 1}
        ]
        linq = Linq(items)
        assert_equal(
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
        assert_equal(
            linq
            .order_by(key_f=lambda obj: (obj['x'], obj['y']), desc=True),
            Linq([{'x': 3, 'y': 4}, {'x': 1, 'y': 2}, {'x': 1, 'y': 1}])
        )

    def test_inject(self):
        linq = Linq([1, 2, 3, 4])
        # 0 - 1 - 2 - 3 - 4
        assert_equal(linq.inject(0, lambda res, val: res - val), -10)
        assert_equal(linq.inject(0, lambda res, val: res - val), -10)

    def test_inject2(self):
        linq = Linq([1, 2, 3, 4])
        # the equare of 0 - 1 - 2 - 3 - 4
        assert_equal(
            linq.inject(0, lambda res, val: res - val, last_f=lambda x: x * x),
            100)
        assert_equal(
            linq.inject(0, lambda res, val: res - val, last_f=lambda x: x * x),
            100)

    def test_join1(self):
        persons = Linq([
            {"name": "person1", "person_id": 1},
            {"name": "person2", "person_id": 2}
        ])
        dogs = Linq([
            {"name": "dog1", "person_id": 1},
            {"name": "dog2", "person_id": 2},
            {"name": "dog3", "person_id": 1},
            {"name": "dog4", "person_id": 2},
        ])
        assert_equal(
            persons.join(
                dogs,
                lambda p: p["person_id"],
                lambda d: d["person_id"],
                lambda p, d: {
                    "person": p["name"],
                    "dog": d["name"],
                }
            ),
            Linq([
                {"person": "person1", "dog": "dog1"},
                {"person": "person1", "dog": "dog3"},
                {"person": "person2", "dog": "dog2"},
                {"person": "person2", "dog": "dog4"}
            ])
        )

    def test_join2(self):
        persons = Linq([
            {"name": "person1", "person_id": 1},
            {"name": "person2", "person_id": 2}
        ])
        dogs = Linq([
            {"name": "dog1", "person_id": 1},
            {"name": "dog2", "person_id": 2},
            {"name": "dog3", "person_id": 1},
            {"name": "dog4", "person_id": 3},
        ])
        assert_equal(
            persons.join(
                dogs,
                lambda p: p["person_id"],
                lambda d: d["person_id"],
                lambda p, d: {
                    "person": p["name"],
                    "dog": d["name"],
                }
            ),
            Linq([
                {"person": "person1", "dog": "dog1"},
                {"person": "person1", "dog": "dog3"},
                {"person": "person2", "dog": "dog2"},
            ])
        )

    def test_group_join(self):
        persons = Linq([
            {"name": "person1", "person_id": 1},
            {"name": "person2", "person_id": 2}
        ])
        dogs = Linq([
            {"name": "dog1", "person_id": 1},
            {"name": "dog2", "person_id": 2},
            {"name": "dog3", "person_id": 1},
            {"name": "dog4", "person_id": 2},
        ])
        assert_equal(
            persons.group_join(
                dogs,
                lambda p: p["person_id"],
                lambda d: d["person_id"],
                lambda p, ds: {
                    "person": p["name"],
                    "dogs": ds.select(lambda d: d["name"]),
                }
            ),
            Linq([
                {"person": "person1", "dogs": Linq(["dog1", "dog3"])},
                {"person": "person2", "dogs": Linq(["dog2", "dog4"])},
            ])
        )

    def test_group_join2(self):
        persons = Linq([
            {"name": "person1", "person_id": 1},
            {"name": "person2", "person_id": 2},
            {"name": "person-1", "person_id": -1}
        ])
        dogs = Linq([
            {"name": "dog1", "person_id": 1},
            {"name": "dog2", "person_id": 2},
            {"name": "dog3", "person_id": 1},
            {"name": "dog4", "person_id": 2},
        ])
        assert_equal(
            persons.group_join(
                dogs,
                lambda p: p["person_id"],
                lambda d: d["person_id"],
                lambda p, ds: {
                    "person": p["name"],
                    "dogs": ds.select(lambda d: d["name"]),
                }
            ),
            Linq([
                {"person": "person1", "dogs": Linq(["dog1", "dog3"])},
                {"person": "person2", "dogs": Linq(["dog2", "dog4"])},
                {"person": "person-1", "dogs": Linq()},
            ])
        )

    def test_count(self):
        assert_equal(Linq([2, 4, 6, 8, 10]).count(), 5)

    def test_count2(self):
        assert_equal(
            Linq([2, 4, 6, 8, 10])
            .count(cond_f=lambda n: n > 5),
            3)

    def test_single(self):
        linq = Linq([1])
        assert_equal(linq.single(), 1)
        assert_equal(linq.single(), 1)

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
        assert_equal(linq.single(cond_f=lambda x: x % 2 == 0), 2)

    def test_single_or_default(self):
        linq = Linq([1])
        assert_equal(linq.single_or_default(), 1)

    def test_single_or_default2(self):
        linq = Linq(tuple())
        assert_equal(linq.single_or_default(default=10), 10)

    @raises(IndexError)
    def test_single_or_default3(self):
        linq = Linq(tuple([1, 2]))
        linq.single_or_default(default=10)

    def test_single_or_default4(self):
        linq = Linq([1, 2, 3, 4, 5])
        assert_equal(
            linq.single_or_default(cond_f=lambda x: x % 3 == 0), 3)

    def test_first(self):
        linq = Linq([11, 13, 15, 19])
        assert_equal(linq.first(), 11)
        assert_equal(linq.first(), 11)

    @raises(IndexError)
    def test_first2(self):
        linq = Linq([])
        linq.first()

    def test_first3(self):
        linq = Linq([11, 14, 15, 19])
        assert_equal(linq.first(cond_f=lambda x: x % 2 == 0), 14)
        assert_equal(linq.first(cond_f=lambda x: x % 2 == 0), 14)

    def test_first_or_default(self):
        linq = Linq([11, 13, 15, 19])
        assert_equal(linq.first_or_default(), 11)
        assert_equal(linq.first_or_default(), 11)

    def test_first_or_default2(self):
        linq = Linq([])
        assert_equal(linq.first_or_default(), None)
        assert_equal(linq.first_or_default(default=100), 100)
        assert_equal(linq.first_or_default(default=100), 100)

    def test_first_or_default3(self):
        linq = Linq([11, 14, 15, 19])
        assert_equal(
            linq.first_or_default(cond_f=lambda x: x % 2 == 0),
            14)
        assert_equal(
            linq.first_or_default(cond_f=lambda x: x % 2 == 0),
            14)

    def test_last(self):
        linq = Linq([11, 13, 15, 19])
        assert_equal(linq.last(), 19)
        assert_equal(linq.last(), 19)

    @raises(IndexError)
    def test_last2(self):
        linq = Linq([])
        linq.last()

    def test_last3(self):
        linq = Linq([11, 13, 15, 19])
        assert_equal(linq.last(cond_f=lambda x: x % 3 == 2), 11)
        assert_equal(linq.last(cond_f=lambda x: x % 3 == 2), 11)

    def test_last_or_default(self):
        linq = Linq([11, 13, 15, 19])
        assert_equal(linq.last_or_default(), 19)
        assert_equal(linq.last_or_default(), 19)

    def test_last_or_default2(self):
        linq = Linq([])
        assert_equal(linq.last_or_default(), None)
        assert_equal(linq.last_or_default(default=10), 10)

    def test_last_or_default3(self):
        linq = Linq([11, 13, 15, 19])
        assert_equal(linq.last_or_default(
            default=2, cond_f=lambda x: x > 100), 2)
        assert_equal(linq.last_or_default(), 19)

    def test_element_at(self):
        linq = Linq([11, 13, 15, 19])
        assert_equal(linq.element_at(2), 15)
        assert_equal(linq.element_at(2), 15)

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
        assert_equal(linq.element_at_or_default(2), 15)
        assert_equal(linq.element_at_or_default(2), 15)

    def test_element_at_or_default2(self):
        linq = Linq([11])
        assert_equal(linq.element_at_or_default(2), None)
        assert_equal(linq.element_at_or_default(2, default=3), 3)

    def test_min(self):
        linq = Linq([13, 19, 11, 15])
        assert_equal(linq.min(), 11)
        assert_equal(linq.min(), 11)

    def test_min2(self):
        linq = Linq([13, 18, 11, 100])
        assert_equal(linq.min(key_f=lambda x: x % 4), 100)
        assert_equal(linq.min(key_f=lambda x: x % 4), 100)

    def test_min_all(self):
        linq = Linq(range(5)).concat(Linq(range(4)))
        assert_equal(linq.min_all(), [0, 0])

    def test_min_all2(self):
        linq = Linq(range(5)).concat(Linq(range(4)))
        assert_equal(
            linq.min_all(key_f=lambda x: x % 4),
            Linq([0, 4, 0]))

    def test_min_all3(self):
        assert_equal(Linq().min_all(), Linq())

    def test_max_all(self):
        linq = Linq(range(5)).concat(Linq(range(5)))
        assert_equal(linq.max_all(), Linq([4, 4]))

    def test_max_all2(self):
        linq = Linq(range(10)).concat(Linq(range(20)))
        assert_equal(
            linq.max_all(key_f=lambda n: n % 5),
            Linq([4, 9, 4, 9, 14, 19]))

    def test_max_all3(self):
        assert_equal(Linq().max_all(), Linq())

    @raises(StopIteration)
    def test_min3(self):
        linq = Linq([])
        linq.min()

    def test_max(self):
        linq = Linq([13, 19, 11, 15])
        assert_equal(linq.max(), 19)
        assert_equal(linq.max(), 19)

    def test_max2(self):
        linq = Linq([1, 6, 1, 4, 2, 2])
        assert_equal(linq.max(key_f=lambda x: x % 2), 1)
        assert_equal(linq.max(key_f=lambda x: x % 2), 1)

    @raises(StopIteration)
    def test_max3(self):
        linq = Linq([])
        linq.max()

    def test_sum(self):
        linq = Linq([1, 1, 4, 2, 2])
        assert_equal(linq.sum(), 10)
        assert_equal(linq.sum(), 10)

    def test_sum2(self):
        linq = Linq([1, 1, 4, 2, 2])
        assert_equal(linq.sum(select_f=lambda x: x*x), 26)
        assert_equal(linq.sum(select_f=lambda x: x*x), 26)

    def test_sum3(self):
        linq = Linq([])
        assert_equal(linq.sum(), 0)

    def test_average(self):
        linq = Linq([1.0, 1.0, 4.0, 2.0, 2.0])
        ave = linq.average()
        assert_true(2 - 0.0002 < ave and ave < 2 + 0.0002)

    def test_average2(self):
        linq = Linq([1.0, 1.0, 4.0, 2.0, 2.0])
        ave = linq.average(select_f=lambda x: x*x)
        assert_true(5.2 - 0.0002 < ave and ave < 5.2 + 0.0002)

    @raises(ZeroDivisionError)
    def test_average3(self):
        linq = Linq([])
        linq.average()

    def test_contain(self):
        linq = Linq([1, 6, 1, 4, 2, 2])
        assert_true(linq.contains(2))
        assert_true(linq.contains(2))

    def test_contain2(self):
        linq = Linq([1, 6, 1, 4, 2, 2])
        assert_false(linq.contains(100))
        assert_false(linq.contains(100))

    def test_contain3(self):
        linq = Linq([1, 2, 3])
        assert_true(linq.contains(101, key_f=lambda n: n % 100))
        assert_false(linq.contains(100, key_f=lambda n: n % 100))

    def test_all(self):
        linq = Linq([1, 1, 3, 4, 5, 7, 9, 11])
        assert_false(linq.all(lambda x: x % 2 == 1))
        assert_false(linq.all(lambda x: x % 2 == 1))

    def test_all2(self):
        linq = Linq([1, 1, 3, 5, 7, 9, 11])
        assert_true(linq.all(lambda x: x % 2 == 1))
        assert_true(linq.all(lambda x: x % 2 == 1))

    def test_any(self):
        linq = Linq([])
        assert_false(linq.any())
        assert_false(linq.any())

    def test_any2(self):
        linq = Linq([1])
        assert_true(linq.any())
        assert_true(linq.any())

    def test_any3(self):
        linq = Linq([2, 3, 4, 5])
        assert_true(linq.any(cond_f=lambda x: x % 2 == 0))
        assert_true(linq.any(cond_f=lambda x: x % 2 == 0))

    def test_any4(self):
        linq = Linq([2, 3, 4, 5])
        assert_false(linq.any(cond_f=lambda x: x > 10))
        assert_false(linq.any(cond_f=lambda x: x > 10))

    def test_group_by(self):
        linq = Linq(range(6))
        assert_equal(
            linq.group_by(lambda n: n % 2),
            IGroup([
                IPair(0, Linq([0, 2, 4])),
                IPair(1, Linq([1, 3, 5]))
            ]))

    def test_to_lookup(self):
        foods = Linq([
            {"name": "natto", "department": "Legumeidae"},
            {"name": "tomato", "department": "Solanaceae"},
            {"name": "Kidney beans", "department": "Legumeidae"}
        ])
        assert_equal(
            foods.to_lookup(
                key_f=lambda f: f["department"],
                value_f=lambda f: f["name"]),
            ILookup({
                "Legumeidae": Linq(["natto", "Kidney beans"]),
                "Solanaceae": Linq(["tomato"])
            })
        )

    def test_to_lookup2(self):
        natto = {"name": "natto", "department": "Legumeidae"}
        tomato = {"name": "tomato", "department": "Solanaceae"}
        kidney_beans = {"name": "Kidney beans", "department": "Legumeidae"}
        assert_equal(
            Linq([natto, tomato, kidney_beans]).to_lookup(
                key_f=lambda f: f["name"]),
            ILookup({
                "natto": Linq([natto]),
                "tomato": Linq([tomato]),
                "Kidney beans": Linq([kidney_beans])}))

    def test_to_lookup3(self):
        assert_equal(
            Linq(range(10)).to_lookup(value_f=lambda n: n % 3),
            ILookup({
                0: Linq([0]),
                1: Linq([1]),
                2: Linq([2]),
                3: Linq([0]),
                4: Linq([1]),
                5: Linq([2]),
                6: Linq([0]),
                7: Linq([1]),
                8: Linq([2]),
                9: Linq([0])
            })
        )

    def test_to_list(self):
        assert_equal(Linq([1]).to_list(), [1])
        assert_equal(Linq([1, 1, 2, 3, 5]).to_list(), [1, 1, 2, 3, 5])

    def test_copy(self):
        linq = Linq(range(10))
        linq_copied = linq.copy()
        assert_true(linq is not linq_copied)
        assert_equal(linq, linq_copied)

    def test_to_set(self):
        assert_equal(Linq([1, 1, 2, 3, 5]).to_set(), {1, 1, 2, 3, 5})

    def test_to_dict(self):
        assert_equal(
            Linq(range(4)).to_dict(key_f=lambda x: x, value_f=lambda x: x * x),
            {0: 0, 1: 1, 2: 4, 3: 9}
        )

    def test_to_dict2(self):
        assert_equal(
            Linq(range(4)).to_dict(value_f=lambda x: x * x),
            {0: 0, 1: 1, 2: 4, 3: 9}
        )

    def test_to_dict3(self):
        assert_equal(
            Linq(range(4)).to_dict(key_f=lambda x: x * x),
            {0: 0, 1: 1, 4: 2, 9: 3}
        )

    @raises(ValueError)
    def test_to_dict4(self):
        Linq(range(4)).to_dict(key_f=lambda _: 1)

    def test_add(self):
        linq1 = Linq([1, 2])
        linq2 = Linq([3, 4])
        linq = linq1 + linq2
        assert_is_instance(linq, Linq)
        assert_equal(linq.to_list(), [1, 2, 3, 4])

    def test_slice(self):
        linq = Linq(range(5))
        assert_true(linq[3] == 3)

    def test_slice2(self):
        linq = Linq()
        assert_true(isinstance(linq[:], Linq))
        assert_true(linq[:] is not linq)

    def test_str0(self):
        assert_equal(str(Linq([])), 'Linq<>')

    def test_str1(self):
        assert_equal(str(Linq([1])), 'Linq<1>')

    def test_str2(self):
        assert_equal(str(Linq([1, 2])), 'Linq<1, 2>')

    def test_repr0(self):
        assert_equal(repr(Linq([])), 'Linq<>')

    def test_repr1(self):
        assert_equal(repr(Linq([1])), 'Linq<1>')

    def test_repr2(self):
        assert_equal(repr(Linq([1, 2])), 'Linq<1, 2>')
