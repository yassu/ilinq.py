#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from nose.tools import raises
from ilinq.igroup import IPair, IGroup
from ilinq.ilinq import Linq


class TestIPair(unittest.TestCase):
    def test_init(self):
        IPair(0, Linq([range(3)]))

    @raises(ValueError)
    def test_init2(self):
        IPair(0, 1)

    def test_key(self):
        pair = IPair(0, Linq([1]))
        self.assertEqual(pair.key, 0)

    def test_values(self):
        pair = IPair(0, Linq([1]))
        self.assertEqual(pair.values, Linq([1]))

    def test_str(self):
        self.assertEqual(str(IPair(0, Linq([1]))), '{0: Linq<1>}')

    def test_repr(self):
        self.assertEqual(repr(IPair(0, Linq([1]))), 'IPair{0: Linq<1>}')

    def test_eq(self):
        self.assertEqual(IPair(0, Linq([0, 1])), IPair(0, Linq([0, 1])))


class TestIGroup(unittest.TestCase):
    def test_init(self):
        IGroup([
            IPair(0, Linq([0, 1, 2]))
        ])

    def test_keys(self):
        group = IGroup([
            IPair(0, Linq([0, 1, 2]))
        ])
        self.assertEqual(group.keys, [0])

    def test_keys2(self):
        group = IGroup([
            IPair(0, Linq([0, 1, 2])),
            IPair(1, Linq([0, 1, 3]))
        ])
        self.assertEqual(group.keys, [0, 1])

    def test_values(self):
        group = IGroup([
            IPair(0, Linq([0, 1, 2])),
            IPair(1, Linq([0, 1, 3]))
        ])
        self.assertEqual(
            group.values,
            [
                Linq([0, 1, 2]),
                Linq([0, 1, 3])
            ]
        )
