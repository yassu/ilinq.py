#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from nose.tools import raises
from ilinq.igroup import IPair


class TestLinq(unittest.TestCase):
    def test_init(self):
        IPair(0, 1)

    def test_key(self):
        pair = IPair(0, 1)
        self.assertEqual(pair.key, 0)

    def test_value(self):
        pair = IPair(0, 1)
        self.assertEqual(pair.value, 1)

    def test_str(self):
        self.assertEqual(str(IPair(0, 1)), '{0: 1}')

    def test_eq(self):
        self.assertEqual(IPair(0, 1), IPair(0, 1))
