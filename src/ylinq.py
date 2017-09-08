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

    def order_by(self, key=None, desc=False):
        return Linq(sorted(list(self), key=key, reverse=desc))

    def inject(self, initial_value, func):
        res = initial_value
        list_ = deepcopy(list(self._iter))
        for item in list_:
            res = func(res, item)
        return res

    def to_list(self):
        return list(self._iter)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iter)
