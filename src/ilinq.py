#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy


class Linq:
    def __init__(self, i):
        self._iter = iter(i)

    def where(self, filter_func):
        def where_generator():
            for item in self._iter:
                if filter_func(item):
                    yield item
        return Linq(where_generator())

    def select(self, select_func):
        def select_generator():
            for item in self._iter:
                yield select_func(item)
        return Linq(select_generator())

    def take(self, num):
        def take_generator():
            for item, _ in zip(self._iter, range(num)):
                yield item
        return Linq(take_generator())

    def distinct(self):
        def distinct_generator():
            list_ = list()
            for item in self._iter:
                if item not in list_:
                    list_.append(item)
                    yield item
        return Linq(distinct_generator())

    def order_by(self, key=None, desc=False):
        return Linq(sorted(list(self), key=key, reverse=desc))

    def inject(self, initial_value, func):
        res = initial_value
        list_ = list(deepcopy(self._iter))
        for item in list_:
            res = func(res, item)
        return res

    def count(self):
        return len(list(deepcopy(self._iter)))

    def first(self):
        iter_ = deepcopy(self._iter)
        return next(iter_)

    def single(self):
        list_ = deepcopy(self).take(2).to_list()
        if len(list_) == 0:
            raise IndexError('This linq is empty.')
        elif len(list_) == 2:
            raise IndexError('This linq is more long.')
        return list_[0]

    def first_or_default(self, default=None):
        try:
            return self.first()
        except StopIteration:
            return default

    def last(self):
        return list(deepcopy(self._iter))[-1]

    def last_or_default(self, default=None):
        try:
            return self.last()
        except IndexError:
            return default

    def element_at(self, ind):
        list_ = deepcopy(self).take(ind + 1).to_list()
        if len(list_) == ind + 1:
            return list_[ind]
        raise IndexError("This linq doesn't have {} items.".format(ind))

    def element_at_or_default(self, num, default=None):
        try:
            return self.element_at(num)
        except IndexError:
            return default

    def min(self, key=lambda x: x):
        return min(list(deepcopy(self._iter)), key=key)

    def max(self, key=lambda x: x):
        return max(list(deepcopy(self._iter)), key=key)

    def sum(self, func=lambda x: x):
        iter_ = deepcopy(self).select(func)
        return sum(iter_)

    def average(self, func=lambda x: x):
        return self.sum(func=func)/self.count()

    def contains(self, item):
        return item in list(deepcopy(self._iter))

    def all(self, cond_func):
        iter_ = deepcopy(self._iter)
        for item in iter_:
            if cond_func(item) is False:
                return False
        return True

    def any(self, cond_func=lambda x: True):
        iter_ = deepcopy(self._iter)
        for item in iter_:
            if cond_func(item):
                return True
        return False

    def to_list(self):
        return list(self._iter)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iter)
