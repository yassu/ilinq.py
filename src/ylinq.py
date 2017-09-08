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

    def to_list(self):
        return list(self._iter)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iter)
