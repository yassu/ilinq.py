#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from functools import reduce


class Linq(list):
    def where(self, cond_func):
        list_ = self[:]
        return Linq([item for item in list_ if cond_func(item)])

    def select(self, select_func):
        return Linq([select_func(item) for item in self[:]])

    def select_many(self, select_func):
        return reduce(
            lambda x, y: x + y, [select_func(item) for item in self[:]])

    def take(self, num):
        return Linq([self[j] for j in range(min(num, len(self)))])

    def concat(self, *linqs):
        res = self
        for linq in linqs:
            res = Linq(res.to_list() + linq.to_list())
        return res

    def default_if_empty(self, default=None):
        list_ = Linq(self[:]).take(1)
        if len(list_) == 1:
            return Linq(self[:])
        else:
            return Linq([default])

    @staticmethod
    def repeat(obj, num):
        return Linq([obj] * num)

    def distinct(self, key_func=None):
        list_ = list()
        val_list = list()
        for item in self[:]:
            val = item if key_func is None else key_func(item)
            if val not in val_list:
                list_.append(item)
                val_list.append(val)
        return Linq(list_)

    def except_(self, other, key_func=None):
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
        return key_func(item) in [key_func(item) for item in self]

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
