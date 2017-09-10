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
    def val(self):
        return self._value
