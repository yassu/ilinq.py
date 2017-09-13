#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides Linq class, which is a python version of linq like c#.
"""

from collections import defaultdict
from functools import reduce


class Linq(list):
    """ class which is similar to be in c# """
    def where(self, cond_func):
        """
        Return the Linq instance filtered by cond_func.

        >>> Linq(range(10 + 1)).where(lambda n: n % 5 == 0)
        Linq<0, 5, 10>
        """
        list_ = self[:]
        return Linq([item for item in list_ if cond_func(item)])

    def select(self, select_func):
        """
        Return the linq instance selected by select_func.

        >>> Linq(range(10 + 1)).select(lambda n: n % 3)
        Linq<0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1>
        """
        return Linq([select_func(item) for item in self[:]])

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

    def order_by(self, key_func=None, desc=False):
        return Linq(sorted(self[:], key=key_func, reverse=desc))

    def inject(self, initial_value, func, last_func=None):
        res = initial_value
        for item in self[:]:
            res = func(res, item)
        return res if last_func is None else last_func(res)

    def count(self, cond_func=lambda x: True):
        return len(self.where(cond_func))

    def first(self, cond_func=lambda x: True):
        for item in self[:]:
            if cond_func(item):
                return item
        raise IndexError('This linq with condition is Empty.')

    def first_or_default(self, default=None, cond_func=lambda x: True):
        for item in self:
            if cond_func(item):
                return item
        return default

    def single(self, cond_func=lambda x: True):
        obj = self.where(cond_func)
        if obj.count() == 0:
            raise IndexError('This linq with condition is empty.')
        elif obj.count() == 2:
            raise IndexError('This linq with condition is more long.')
        return obj[0]

    def single_or_default(self, default=None, cond_func=lambda x: True):
        obj = self.where(cond_func)
        if obj.count() == 0:
            return default
        return obj.single()

    def last(self, func=lambda x: True):
        return self.where(func)[-1]

    def last_or_default(self, default=None, cond_func=lambda x: True):
        try:
            return self.where(cond_func).last()
        except IndexError:
            return default

    def element_at(self, ind):
        list_ = self.take(ind + 1).to_list()
        if len(list_) == ind + 1:
            return list_[ind]
        raise IndexError("This linq doesn't have {} items.".format(ind))

    def element_at_or_default(self, num, default=None):
        try:
            return self.element_at(num)
        except IndexError:
            return default

    def min(self, key_func=lambda x: x):
        try:
            return min(self, key=key_func)
        except ValueError:
            raise StopIteration('This linq is empty.')

    def max(self, key_func=lambda x: x):
        try:
            return max(self, key=key_func)
        except ValueError:
            raise StopIteration('This linq is empty.')

    def sum(self, cond_func=lambda x: x, select_func=None):
        list_ = self if select_func is None else \
            Linq([select_func(item) for item in self])
        return sum(list_.select(cond_func))

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
