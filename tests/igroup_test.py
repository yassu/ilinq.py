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

    def test_val(self):
        pair = IPair(0, 1)
        self.assertEqual(pair.val, 1)
