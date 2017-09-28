#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from nose.tools import assert_equal, raises
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
        assert_equal(pair.key, 0)

    def test_values(self):
        pair = IPair(0, Linq([1]))
        assert_equal(pair.values, Linq([1]))

    def test_str(self):
        assert_equal(str(IPair(0, Linq([1]))), '{0: Linq<1>}')

    def test_repr(self):
        assert_equal(repr(IPair(0, Linq([1]))), 'IPair{0: Linq<1>}')

    def test_eq(self):
        assert_equal(IPair(0, Linq([0, 1])), IPair(0, Linq([0, 1])))


class TestIGroup(unittest.TestCase):
    def test_init(self):
        assert_equal(IGroup().count(), 0)

    def test_init2(self):
        IGroup([
            IPair(0, Linq([0, 1, 2]))
        ])

    @raises(ValueError)
    def test_init3(self):
        IGroup([
            0,
            IPair(1, Linq([1, 2, 3]))
        ])

    @raises(ValueError)
    def test_init4(self):
        IGroup([
            IPair(0, Linq([1, 2, 3])),
            IPair(1, Linq([2, 3, 4])),
            IPair(1, Linq([2, 3, 4]))
        ])

    def test_keys(self):
        group = IGroup([
            IPair(0, Linq([0, 1, 2]))
        ])
        assert_equal(group.keys, [0])

    def test_keys2(self):
        group = IGroup([
            IPair(0, Linq([0, 1, 2])),
            IPair(1, Linq([0, 1, 3]))
        ])
        assert_equal(group.keys, [0, 1])

    def test_values(self):
        group = IGroup([
            IPair(0, Linq([0, 1, 2])),
            IPair(1, Linq([0, 1, 3]))
        ])
        assert_equal(
            group.values,
            [
                Linq([0, 1, 2]),
                Linq([0, 1, 3])
            ]
        )

    def test_str(self):
        group = IGroup([
            IPair(0, Linq([0, 1, 2])),
            IPair(1, Linq([0, 1, 3]))
        ])
        assert_equal(
            str(group),
            'IGroup<{0: Linq<0, 1, 2>}, {1: Linq<0, 1, 3>}>')
