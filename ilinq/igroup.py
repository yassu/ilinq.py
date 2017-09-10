#!/usr/bin/env python
# -*- coding: utf-8 -*-


class IPair(object):
    def __init__(self, key, value):
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    def __str__(self):
        return '{%s: %s}' % (self.key, self.value)

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value
