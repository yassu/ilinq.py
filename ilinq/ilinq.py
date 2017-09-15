#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides Linq class, which is a python version of linq like c#.
"""

from collections import defaultdict
from functools import reduce


class Linq(list):
    """  Class for handling Linq like C# """
    def where(self, cond_func=None):
        """
        Return the Linq instance filtered by cond_func.
        And if cond_func is None, return all items.

        >>> Linq(range(10 + 1)).where(lambda n: n % 5 == 0)
        Linq<0, 5, 10>
        """
        list_ = self[:]
        return Linq([
            item for item in list_
            if cond_func is None or cond_func(item)])

    def where_in(self, list_, select_func=None):
        """
        return items which the condition that select_func(item) in list_

        >>> Linq([1, 3, 5, 100]).where_in([1, 2, 3])
        Linq<1, 3>
        >>> Linq([1, 3, 5, 100]).where_in(
            [1, 2, 3],
            select_func=lambda x: x % 2)
        Linq<1, 3, 5>
        """
        return self.where(
            lambda x: x in list_ if select_func is None else
            select_func(x) in list_)

    def select(self, select_func=None):
        """
        Return the linq instance selected by select_func.

        >>> Linq(range(10 + 1)).select(lambda n: n % 3)
        Linq<0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1>
        """
        return Linq([
            item if select_func is None else
            select_func(item) for item in self[:]])

    def select_many(self, select_func):
        """
        Return the linq instance selected by select_func and flatten.

        >>> linq = Linq([
            {"name": "yassu", "ids": (12, 13)},
            {"name": "aiya",  "ids": (20, 21)}])
        >>> linq.select_many(lambda obj: obj["ids"])
        (12, 13, 20, 21)
        """
        return reduce(
            lambda x, y: x + y, [select_func(item) for item in self[:]])

    def take(self, num):
        """
        Return first num numbers of this object.

        >>> linq = Linq(range(10))
        >>> linq.take(4)
        Linq<0, 1, 2, 3>
        >>> linq.take(100)
        Linq<0, 1, 2, 3, 4, 5, 6, 7, 8, 9>
        """
        return Linq([self[j] for j in range(min(num, len(self)))])

    def concat(self, *linqs):
        """
        >>> linq = Linq(range(4))
        >>> linq.concat(Linq(range(5)).select(lambda x: x*x))
        Linq<0, 1, 2, 3, 0, 1, 4, 9, 16>

        >>> linq1 = Linq(range(5))
        >>> linq2 = Linq(range(4)).select(lambda x: x * x)
        >>> linq3 = Linq(range(3)).select(lambda x: x * x * x)
        >>> linq1.concat(linq2, linq3)
        Linq<0, 1, 2, 3, 4, 0, 1, 4, 9, 0, 1, 8>
        """
        res = self
        for linq in linqs:
            res = Linq(res.to_list() + linq.to_list())
        return res

    def default_if_empty(self, default=None):
        """
        if self is empty, return Linq([default]) else self.

        >>> Linq(range(3)).default_if_empty()
        Linq<0, 1, 2>
        >>> Linq(range(3)).default_if_empty("default")
        Linq<0, 1, 2>

        >>> Linq([]).default_if_empty()
        Linq<None>
        >>> Linq([]).default_if_empty("default")
        Linq<default>
        """
        list_ = Linq(self[:]).take(1)
        if len(list_) == 1:
            return Linq(self[:])
        else:
            return Linq([default])

    @staticmethod
    def repeat(obj, num):
        """
        return Linq instance which has num objs.

        >>> Linq.repeat('Hello', 5)
        Linq<Hello, Hello, Hello, Hello, Hello>
        """
        return Linq([obj] * num)

    def distinct(self, key_func=None):
        """
        return self deleted duplicates

        >>> linq1 = Linq(range(4))
        >>> linq2 = Linq(range(5)).select(lambda x: x * x)
        >>> linq1.concat(linq2).distinct()
        Linq<0, 1, 2, 3, 4, 9, 16>
        """
        list_ = list()
        val_list = list()
        for item in self[:]:
            val = item if key_func is None else key_func(item)
            if val not in val_list:
                list_.append(item)
                val_list.append(val)
        return Linq(list_)

    def except_(self, other, key_func=None):
        """
        If key_func is None, return self values except for other values.

        >>> Linq(range(10)).except_(Linq(range(4)))
        Linq<4, 5, 6, 7, 8, 9>

        If key_func is not None, return self values with condition that
        key_func(item) doesn't contain key_func(other_item) items.

        >>> linq1 = Linq([1, 2, -3, -4, -5])
        >>> linq2 = Linq([2, 3, 5, 7, 6])
        >>> linq1.except_(linq2, key_func=lambda x: abs(x))
        Linq<1, -4>
        """
        res = list()
        for item in self[:]:
            val = item if key_func is None else key_func(item)
            if val not in other:
                res.append(item)
        return Linq(res)

    def intersect(self, other):
        """
        >>> linq1 = Linq([2.0, -2.0, 2.1, -2.2, 2.3, 2.4, 2.5, 2.3])
        >>> linq2 = Linq([2.1, 2.2])
        >>> linq1.intersect(linq2)
        Linq<2.1>
        """
        return Linq([item for item in self if item in other])

    def order_by(self, key_func=None, desc=False):
        """
        If desc=False and key_func=None, sort in ascending order.

        >>> Linq([1.1, 2.3, -2, 5.3, 1.3]).order_by()
        Linq<-2, 1.1, 1.3, 2.3, 5.3>

        If desc=True, sort in descending order

        >>> Linq([1.1, 2.3, -2, 5.3, 1.3]).order_by(desc=True)
        Linq<5.3, 2.3, 1.3, 1.1, -2>

        If key_func is not None, sort by result of key_func

        >>> linq = Linq([
                {"name": "person1", "age": 23},
                {"name": "person2", "age": 25},
                {"name": "person3", "age": 21}])
        >>> linq.order_by(key_func=lambda person: person["age"])
        Linq<
            {'name': 'person3', 'age': 21},
            {'name': 'person1', 'age': 23},
            {'name': 'person2', 'age': 25}>
        """
        return Linq(sorted(self[:], key=key_func, reverse=desc))

    def inject(self, initial_value, func, last_func=None):
        """
        return the result of
        func(func(func(initial_value, self[0]), self[1]) .. self[length - 1])
        filtered by last_func.

        >>> Linq(range(100 + 1)).inject(0, lambda res, x: res + x)
        5050
        >>> Linq(range(100 + 1)).inject(
            0,
            lambda res, x: res + x,
            last_func=lambda x: x + 100)
        5150
        """
        res = initial_value
        for item in self[:]:
            res = func(res, item)
        return res if last_func is None else last_func(res)

    def count(self, cond_func=None):
        """
        return the length with condition that cond_func(item).

        >>> Linq(range(10)).count()
        10
        >>> Linq(range(10)).count(lambda x: x >= 8)
        2
        """
        return len(self.where(
            cond_func if cond_func is not None else
            lambda x: True))

    def first(self, cond_func=None):
        """
        return the first element with cond_func(item)

        >>> Linq([3, 2, 5, 8]).first()
        3
        >>> Linq([3, 2, 5, 8]).first(cond_func=lambda x: x % 2 == 0)
        2
        """
        for item in self[:]:
            if cond_func is None or cond_func(item):
                return item
        raise IndexError('This linq with condition is Empty.')

    def first_or_default(self, default=None, cond_func=None):
        """
        return the first element with cond_func(item) and default value
        is default.

        >>> Linq([3, 2, 5, 8]).first_or_default()
        3
        >>> Linq([3, 2, 5, 8]).first_or_default(
            cond_func=lambda x: x % 2 == 0)
        2
        >>> Linq([3, 2, 5, 8]).first_or_default(
            cond_func=lambda x: x > 100,
            default=100)
        100
        """
        for item in self:
            if cond_func is None or cond_func(item):
                return item
        return default

    def single(self, cond_func=None):
        """
        If this object consists of one object, return this object.
        Otherwise, error is occured.

        >>> Linq([]).single()
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "/Users/yuki_yasuda/dev/ilinq.py/ilinq/ilinq.py", line 95, in
          single @staticmethod
        IndexError: This linq with condition is empty.
        >>> Linq([12]).single()
        12
        >>> Linq([12, 15]).single()
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "/Users/yuki_yasuda/dev/ilinq.py/ilinq/ilinq.py", line 97, in
        single
        IndexError: This linq with condition is more long.
        """
        obj = self.where(cond_func)
        if obj.count() == 0:
            raise IndexError('This linq with condition is empty.')
        elif obj.count() == 2:
            raise IndexError('This linq with condition is more long.')
        return obj[0]

    def single_or_default(self, default=None, cond_func=None):
        """
        If this obj consists only one object, return this object.

        If this obj is empty, return default.

        If this obj consists more than one objects, error is occured.

        >>> Linq([]).single_or_default(16)
        16
        >>> Linq([32]).single_or_default()
        32
        >>> Linq([12, 35]).single_or_default()
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "/Users/yuki_yasuda/dev/ilinq.py/ilinq/ilinq.py", line 104, in
        single_or_default
            \"\"\"
          File "/Users/yuki_yasuda/dev/ilinq.py/ilinq/ilinq.py", line 97, in
        single
            @staticmethod
        IndexError: This linq with condition is more long.
        """
        obj = self.where(cond_func)
        if obj.count() == 0:
            return default
        return obj.single()

    def last(self, func=None):
        """
        return the first element with cond_func(item)

        >>> Linq([3, 2, 5, 8]).last()
        8
        >>> Linq([3, 2, 5, 8]).last(lambda x: x % 4 == 1)
        5
        """
        return self.where(func)[-1]

    def last_or_default(self, default=None, cond_func=None):
        """
        return the last element with cond_func(item) and default value
        is default.

        >>> Linq([3, 2, 5, 8]).last_or_default()
        8
        >>> Linq([3, 2, 5, 8]).last_or_default(cond_func=lambda x: x % 2 == 1)
        5
        >>> Linq([3, 2, 5, 8]).last_or_default(
            cond_func=lambda x: x > 100,
            default=-100)
        -100
        """
        try:
            return self.where(cond_func).last()
        except IndexError:
            return default

    def element_at(self, ind):
        """
        return the element at ind index.

        >>> Linq([3, 2, 5, 8]).element_at(2)
        5
        """
        list_ = self.take(ind + 1).to_list()
        if len(list_) == ind + 1:
            return list_[ind]
        raise IndexError("This linq doesn't have {} items.".format(ind))

    def element_at_or_default(self, num, default=None):
        """
        If there is num-th element, return this.
        Else return default value.

        >>> from ilinq.ilinq import Linq
        >>> linq = Linq([1, 2])
        >>> linq.element_at_or_default(0)
        1
        >>> linq.element_at_or_default(3)
        # None
        """
        try:
            return self.element_at(num)
        except IndexError:
            return default

    def min(self, key_func=None):
        """
        return minimal value in this object.
        if key_func is defined, return minimal value by key_func(item).

        >>> Linq([-1, 2, 3, -4.3, 2]).min()
        -4.3
        >>> Linq([-1, 2, 3, -4.3, 2]).min(abs)
        -1
        """
        try:
            return min(
                self,
                key=lambda x: x if key_func is None else key_func(x))
        except ValueError:
            raise StopIteration('This linq is empty.')

    def max(self, key_func=None):
        """
        return maximal value in this object.
        if key_func is defined, return minimal value by key_func(item).

        >>> Linq([-1, 2, 3, -4.3, 2]).max()
        3
        >>> Linq([-1, 2, 3, -4.3, 2]).max(abs)
        -4.3
        """
        try:
            return max(
                self,
                key=lambda x: x if key_func is None else key_func(x))
        except ValueError:
            raise StopIteration('This linq is empty.')

    def sum(self, filter_func=None, select_func=None):
        """
        return filter_func(total of select_func(item))

        >>> Linq(range(100 + 1)).sum()
        5050
        """
        res = sum(self.select(select_func).select())
        return res if filter_func is None else filter_func(res)

    def average(self, select_func=lambda x: x):
        return self.sum(select_func=select_func) / self.count()

    def contains(self, item, key_func=lambda x: x):
        return key_func(item) in [key_func(item_) for item_ in self]

    def all(self, cond_func):
        for item in self:
            if cond_func(item) is False:
                return False
        return True

    def any(self, cond_func=lambda x: True):
        for item in self:
            if cond_func(item):
                return True
        return False

    def group_by(self, grouping_func):
        from ilinq.igroup import IPair, IGroup
        group = IGroup()
        group_dict = defaultdict(lambda: Linq([]))
        for item in self[:]:
            group_dict[grouping_func(item)].append(item)

        for key, values in group_dict.items():
            group.append(IPair(key, values))
        return group

    def to_list(self):
        return list(self)

    def copy(self):
        return Linq(self[:])

    def to_set(self):
        return set(self)

    def __str__(self):
        s = 'Linq<'
        for item in self:
            s += str(item)
            s += ', '
        if self.count() > 0:
            s = s[:-2]
        return s + '>'

    def __repr__(self):
        return str(self)
