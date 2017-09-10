#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Linq(list):
    def where(self, filter_func):
        list_ = self[:]
        return Linq([item for item in list_ if filter_func(item)])

    def select(self, select_func):
        return Linq([select_func(item) for item in self[:]])

    def take(self, num):
        return Linq([self[j] for j in range(min(num, len(self)))])

    def distinct(self):
        list_ = list()
        for item in self[:]:
            if item not in list_:
                list_.append(item)
        return Linq(list_)

    def order_by(self, key=None, desc=False):
        return Linq(sorted(self[:], key=key, reverse=desc))

    def inject(self, initial_value, func):
        res = initial_value
        for item in self[:]:
            res = func(res, item)
        return res

    def count(self):
        return len(self)

    def first(self, func=lambda x: True):
        for item in self[:]:
            if func(item):
                return item
        raise IndexError('This linq with condition is Empty.')

    def first_or_default(self, default=None, func=lambda x: True):
        for item in self:
            if func(item):
                return item
        return default

    def single(self):
        if self.count() == 0:
            raise IndexError('This linq is empty.')
        elif self.count() == 2:
            raise IndexError('This linq is more long.')
        return self[0]

    def single_or_default(self, default=None):
        if self.count() == 0:
            return default
        return self.single()

    def last(self):
        return self[-1]

    def last_or_default(self, default=None):
        try:
            return self.last()
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

    def min(self, key=lambda x: x):
        try:
            return min(self, key=key)
        except ValueError:
            raise StopIteration('This linq is empty.')

    def max(self, key=lambda x: x):
        try:
            return max(self, key=key)
        except ValueError:
            raise StopIteration('This linq is empty.')

    def sum(self, func=lambda x: x):
        return sum(self.select(func))

    def average(self, func=lambda x: x):
        return self.sum(func=func) / self.count()

    def contains(self, item):
        return item in self

    def all(self, func):
        for item in self:
            if func(item) is False:
                return False
        return True

    def any(self, func=lambda x: True):
        for item in self:
            if func(item):
                return True
        return False

    def to_list(self):
        return list(self)
