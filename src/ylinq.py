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

    def order_by(self, key=None, desc=False):
        return Linq(sorted(list(self), key=key, reverse=desc))

    def inject(self, initial_value, func):
        res = initial_value
        list_ = deepcopy(list(self._iter))
        for item in list_:
            res = func(res, item)
        return res

    def count(self):
        return len(list(self._iter))

    def first(self):
        iter_ = deepcopy(self._iter)
        return next(iter_)

    def last(self):
        return list(self._iter)[-1]

    def min(self, key=lambda x: x):
        return min(list(self._iter), key=key)

    def max(self, key=lambda x: x):
        return max(list(self._iter), key=key)

    def to_list(self):
        return list(self._iter)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iter)
